"""
Code for Non-reversible Parallel Tempering for Deep Posterior Approximation
(c) Wei Deng
Nov 24, 2022

Note that in Bayesian settings, the lr 2e-6 and weight decay 25 are equivalent to lr 0.1 and weight decay 5e-4 in standard setups.
"""

#!/usr/bin/python
import math
import copy
import sys
import os
import time
import csv
import argparse
import random
import collections
from random import shuffle
import pickle

#from tqdm import tqdm ## better progressbar
from math import exp
from sys import getsizeof
import numpy as np

## import pytorch modules
import torch
import torch.optim as optim
from torch.autograd import Variable
import torch.nn as nn
from torchvision import datasets, transforms
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
import torch.utils.data as data
import torchvision.datasets as datasets

## Import helper functions
from tools import BayesEval, StochasticWeightAvg
from SGHMC import SGHMC

CUDA_EXISTS = torch.cuda.is_available()


""" For standard baseline ensemble """
def trainer_vanilla_ensemble(nets, train_loader, test_loader, pars):
    criterion = nn.CrossEntropyLoss()
    samplers = {}
    for idx in range(pars.chains):
        samplers[idx] = optim.SGD(nets[idx].parameters(), lr=pars.lr_min, momentum=pars.momentum, weight_decay=pars.wdecay)
    BMA = BayesEval(pars.data)

    for epoch in range(pars.sn):
        for idx in range(pars.chains):
            nets[idx].train()
        for i, (images, labels) in enumerate(train_loader):
            images = Variable(images).cuda() if CUDA_EXISTS else Variable(images)
            labels = Variable(labels).cuda() if CUDA_EXISTS else Variable(labels)
            for idx in range(pars.chains):
                current_loss = criterion(nets[idx](images), labels)
                samplers[idx].zero_grad()
                current_loss.backward()
                samplers[idx].step()

        """ Report results """
        if epoch % pars.chains == 0:
            for idx in range(pars.chains-1, -1, -1):
                BMA.eval(pars.data, nets[idx], test_loader, criterion, bma=True, uq=True)
            print('Epoch {} lr: {:.4f} Acc: {:0.2f} BMA: {:0.2f} Best Acc: {:0.2f} Best BMA: {:0.2f}'.format(\
                    epoch,  pars.lr_min,    BMA.cur_acc, BMA.bma_acc, BMA.best_cur_acc, BMA.best_bma_acc))
            print('Epoch {} NLL: {:.1f} Best NLL: {:.1f} BMA NLL: {:.1f}  Best BMA NLL: {:.1f}'.format(epoch, BMA.nll, BMA.best_nll, BMA.bma_nll, BMA.best_bma_nll))
        print('')

""" Train baselines cyclic SGHMC + SWAG """
def trainer_cyc_ensemble(nets, train_loader, test_loader, pars):
    criterion = nn.CrossEntropyLoss()
    sampler, BMA, SWAG = SGHMC(nets[0]), BayesEval(pars.data), StochasticWeightAvg(pars.data, cycle=100)

    print('Ensemble the initial modes first for fair comparison')
    for idx in range(pars.chains):
        nets[idx].eval()
        BMA.eval(pars.data, nets[idx], test_loader, criterion, weight=10, bma=True, uq=True, print_tag=False)
        print('Initial ensemble Acc: {:0.2f} BMA: {:0.2f}'.format(BMA.cur_acc, BMA.bma_acc))

    """ the 0.1 learning rate in frequentist is equivalent to 0.1 / N in Bayesian, 
        where N is the number of total data points """
    N, warm = 50000, 0.85
    for epoch in range(pars.sn):
        """ cosine learning rate """
        sub_sn = 100
        base_lr = 0.1 / N
        cur_beta = (epoch % sub_sn) * 1.0 / sub_sn
        sampler.lr = base_lr / 2 * (np.cos(np.pi * min(cur_beta, warm)) + 1)
        if (epoch % sub_sn) * 1.0 / sub_sn == 0:
            print('Cooling down for optimization')
            sampler.T /= 1e10
        elif epoch % sub_sn == int(warm * sub_sn):
            print('Heating up for sampling')
            sampler.T *= 1e10

        nets[0].train()
        for i, (images, labels) in enumerate(train_loader):
            images = Variable(images).cuda() if CUDA_EXISTS else Variable(images)
            labels = Variable(labels).cuda() if CUDA_EXISTS else Variable(labels)
            sampler.net.zero_grad()
            loss = criterion(sampler.net(images), labels) * N
            loss.backward()
            sampler.step(images, labels)

        if cur_beta >= warm:
            SWAG.update(epoch // sub_sn, nets[0], cur_beta, warm)
            if (epoch + 1) % sub_sn == 0 and epoch >= sub_sn - 1:
                SWAG.inference(pars.data, epoch // sub_sn, train_loader, test_loader, criterion, pars.lr_min/N, repeats=10)

            BMA.eval(pars.data, nets[0], test_loader, criterion, bma=True, uq=True)
            print('Epoch {} lr: {:.2e} T: {:.2e} Acc: {:0.2f} BMA: {:0.2f} Best Acc: {:0.2f} Best BMA: {:0.2f}'.format(\
                epoch,  sampler.lr, sampler.T,    BMA.cur_acc, BMA.bma_acc, BMA.best_cur_acc, BMA.best_bma_acc))
            print('Epoch {} NLL: {:.1f} Best NLL: {:.1f} BMA NLL: {:.1f}  Best BMA NLL: {:.1f}'.format(epoch, BMA.nll, BMA.best_nll, BMA.bma_nll, BMA.best_bma_nll))
        else:
            if epoch % 10 == 0:
                BMA.eval(pars.data, nets[0], test_loader, criterion, bma=False, uq=False)
                print('Epoch {} lr: {:.2e} T: {:.2e} Acc: {:0.2f} BMA: {:0.2f} Best Acc: {:0.2f} Best BMA: {:0.2f}'.format(\
                    epoch,  sampler.lr, sampler.T,    BMA.cur_acc, BMA.bma_acc, BMA.best_cur_acc, BMA.best_bma_acc))
            else:
                print('Epoch {} lr: {:.2e} T: {:.2e}'.format(epoch,  sampler.lr, sampler.T))

""" For our proposed parallel tempering methods """
def trainer(nets, train_loader, test_loader, pars):
    criterion = nn.CrossEntropyLoss()

    ratio = (pars.lr_max / pars.lr_min) ** (1. / (pars.chains-1 + 1e-10))
    current_lr =  np.array([round(pars.lr_min * ratio**power, 4) for power in range(pars.chains)])
    print('Initial learning rate {} in ensemble period'.format(' '.join(map(str, current_lr))))
    samplers, BMAS = {}, []
    for idx in range(pars.chains):
        samplers[idx] = optim.SGD(nets[idx].parameters(), lr=current_lr[idx], momentum=pars.momentum, weight_decay=pars.wdecay)
        BMAS.append(BayesEval(pars.data))

    gates = [1] * pars.chains
    cumulative_swap, tentative_swap = [0.] * pars.chains, [0.] * pars.chains
    correction, iters = pars.correction, 0

    if pars.window_custom == 0:
        window = int(np.ceil((np.log(pars.chains) + np.log(np.log(pars.chains))) / -np.log(1 - pars.swap_rate)))
    else:
        window = pars.window_custom
    print('The optimal window size is {}'.format(window))

    """ Calculate the number of round trips """
    index_set = np.arange(pars.chains)
    last_visited = []
    for _ in range(pars.chains):
        last_visited.append(set())

    round_trip, warm_epoch = 0, 5


    start = time.time()

    for idx in [0, 1, 2]:
        print('Ensemble the initial modes first')
        for inner_idx in range(pars.chains):
            nets[inner_idx].eval()
            BMAS[idx].eval(pars.data, nets[inner_idx], test_loader, criterion, weight=10, bma=True, uq=True, print_tag=False)
    for epoch in range(pars.sn):
        for idx in range(pars.chains):
            nets[idx].train()
        for i, (images, labels) in enumerate(train_loader):
            loss_chains, swap_indicator = [0] * pars.chains, [0] * (pars.chains - 1)
            images = Variable(images).cuda() if CUDA_EXISTS else Variable(images)
            labels = Variable(labels).cuda() if CUDA_EXISTS else Variable(labels)

            """ Open the gate to allow a swap in the current """
            if iters % window == 0:
                gates = [1] * pars.chains

            stepsize = min(0.5, pars.gamma / (iters**0.8 + 1000.))
            iters = iters + 1
            """ reset the last learning rate """
            last_lr = copy.deepcopy(current_lr)

            for idx in range(pars.chains):
                current_loss = criterion(nets[idx](images), labels)
                samplers[idx].zero_grad()
                current_loss.backward()
                samplers[idx].step()
                loss_chains[idx] = current_loss.item()

                """ Swap module """ 
                if idx > 0 and pars.swap_rate > 0:
                    swap_indicator[idx-1] = 1. if loss_chains[idx] + correction < loss_chains[idx-1] else 0.
                    tentative_swap[idx] += swap_indicator[idx-1]
                    if (idx % 2 == ((iters // window) % 2)) and gates[idx] == 1 and swap_indicator[idx-1] == 1:
                        """ swap models """
                        temporary = pickle.loads(pickle.dumps(nets[idx-1]))
                        nets[idx-1].load_state_dict(nets[idx].state_dict())
                        nets[idx].load_state_dict(temporary.state_dict())
                        """ swap losses """
                        loss_chains[idx-1], loss_chains[idx] = loss_chains[idx], loss_chains[idx-1]
                        """ swap index to record changes of round trips """
                        index_set[idx-1], index_set[idx] = index_set[idx], index_set[idx-1]

                        """ Close the gate in the current window """
                        gates[idx] = 0

                        cumulative_swap[idx] += 1.
                        """ avoid consecutive swaps """
                        print('Epoch {} Swap chain {} (loss {:0.3f}) with chain {} (loss {:0.3f}) Cumulative swaps {} iters {}'.format(\
                                epoch, idx-1, loss_chains[idx-1], idx, loss_chains[idx], int(cumulative_swap[idx]), iters))

                        """ reset sampler """
                        samplers[idx] = optim.SGD(nets[idx].parameters(), lr=current_lr[idx], momentum=pars.momentum, weight_decay=pars.wdecay)
                        samplers[idx-1] = optim.SGD(nets[idx-1].parameters(), lr=current_lr[idx-1], momentum=pars.momentum, weight_decay=pars.wdecay)

                """ count the number of round trips: visited two ends """
                last_visited[index_set[0]].add(0)
                last_visited[index_set[pars.chains-1]].add(pars.chains-1)

                """ count the number of round trips: returned to the original position """
                if len(last_visited[idx]) == 2 and idx == index_set[idx]:
                    last_visited[idx] = set()
                    round_trip += 1

                """ Adaptive learning rates for equi-acceptance rates """
                for idx in range(1, pars.chains-1):
                    current_lr[idx] = (last_lr[idx-1] + max(0, last_lr[idx] - last_lr[idx-1]) * np.exp((swap_indicator[idx-1] - pars.swap_rate) * stepsize) \
                                     + last_lr[idx+1] - max(0, last_lr[idx+1] - last_lr[idx]) * np.exp((swap_indicator[idx] - pars.swap_rate) * stepsize)) / 2
                    for group in samplers[idx].param_groups:
                        group['lr'] = current_lr[idx]

            correction = correction + (np.mean(swap_indicator) - pars.swap_rate) * stepsize / pars.scale

        """ Report results """
        for idx in range(pars.chains-1, -1, -1):
            BMAS[idx].eval(pars.data, nets[idx], test_loader, criterion, bma=True, uq=False)
            print('Epoch {} Chain {} lr: {:.4f} Acc: {:0.2f} BMA: {:0.2f} Best Acc: {:0.2f} Best BMA: {:0.2f} Loss: {:0.3f} Window {} Trips {} Swaps/tentative/rate/target {}/ {:.1e}/ {:.1e}/ {:.1e} Corrections: {:0.3f}'.format(\
                    epoch, idx, current_lr[idx], BMAS[idx].cur_acc, BMAS[idx].bma_acc, BMAS[idx].best_cur_acc, BMAS[idx].best_bma_acc, \
                    np.array(loss_chains[idx]).sum(), window, round_trip, int(cumulative_swap[idx]), tentative_swap[idx] / iters, cumulative_swap[idx] / iters, pars.swap_rate, correction))
        print('Epoch {} Chain {} NLL: {:.1f} Best NLL: {:.1f} BMA NLL: {:.1f}  Best BMA NLL: {:.1f}'.format(epoch, 0, BMAS[0].nll, BMAS[0].best_nll, BMAS[0].bma_nll, BMAS[0].best_bma_nll))
        print('')

    end = time.time()
    print('Time used {:.2f}s'.format(end - start))
