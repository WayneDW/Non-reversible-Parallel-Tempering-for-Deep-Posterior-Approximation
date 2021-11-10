"""
Code for Non-reversible Parallel Tempering for Uncertainty Approximation
(c) Anonymous authors
Nov 8, 2021
"""

#!/usr/bin/python

import math
import copy
import time
import sys
import os
import timeit
import csv
import argparse
#from tqdm import tqdm ## better progressbar
from math import exp
from sys import getsizeof
import numpy as np
import random
import pickle
## import pytorch modules
import torch
from torch.autograd import Variable
import numpy as np


import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torchvision import datasets, transforms
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
import torch.utils.data as data
import torchvision.datasets as datasets


import models.cifar as cifar_models
from models.cifar import PyramidNet as PYRM

from tools import loader, BayesEval


def main():
    parser = argparse.ArgumentParser(description='Grid search')
    parser.add_argument('-type', default='PT', type=str, help='PT or ensemble or cyclic')
    parser.add_argument('-aug', default=1, type=float, help='Data augmentation or not')
    """ numper of optimization/ sampling epochs """
    parser.add_argument('-sn', default=500, type=int, help='Sampling Epochs')
    parser.add_argument('-wdecay', default=5e-4, type=float, help='Samling weight decay')
    parser.add_argument('-lr', default=0.1, type=float, help='Sampling learning rate')
    parser.add_argument('-momentum', default=0.9, type=float, help='Sampling momentum learning rate')

    """ data, model and batch size """
    parser.add_argument('-data', default='cifar100', dest='data', help='CIFAR10')
    parser.add_argument('-total', default=50000, type=int, help='total data points')
    parser.add_argument('-model', default='resnet', type=str, help='resnet')
    parser.add_argument('-depth', type=int, default=20, help='Model depth.')
    parser.add_argument('-batch', default=256, type=int, help='Batch size')

    parser.add_argument('-lr_gap', default=5, type=float, help='decay of learning rates for simulated annealing')
    parser.add_argument('-warm', default=0.9, type=float, help='warm-up or burn-in')

    """ other settings """
    parser.add_argument('-seed', default=random.randint(1, 1e6), type=int, help='Random Seed')
    parser.add_argument('-gpu', default=0, type=int, help='Default GPU')


    pars = parser.parse_args()
    """ Step 0: Numpy printing setup and set GPU and Seeds """
    print(pars)
    np.set_printoptions(precision=3)
    np.set_printoptions(suppress=True)
    try:
        torch.cuda.set_device(pars.gpu)
    except: # in case the device has only one GPU
        torch.cuda.set_device(0) 
    torch.manual_seed(pars.seed)
    torch.cuda.manual_seed(pars.seed)
    np.random.seed(pars.seed)
    random.seed(pars.seed)
    torch.backends.cudnn.deterministic=True

    """ Step 1: Preprocessing """
    if not torch.cuda.is_available():
        exit("CUDA does not exist!!!")
    if pars.model == 'resnet':
        if pars.data == 'cifar10':
            net = cifar_models.__dict__['resnet'](num_classes=10, depth=pars.depth).cuda()
        elif pars.data == 'cifar100':
            net = cifar_models.__dict__['resnet'](num_classes=100, depth=pars.depth).cuda()

    """ Step 2: Load Data """
    train_loader, test_loader = loader(pars.batch, pars.batch, pars)

    """ Step 3: Initialize models (only train and save one checkpoint) """
    CUDA_EXISTS = torch.cuda.is_available()


    criterion = nn.CrossEntropyLoss()
    sampler = optim.SGD(net.parameters(), lr=pars.lr, momentum=pars.momentum, weight_decay=pars.wdecay)
    BMA = BayesEval(pars.data)
    cur_lr = pars.lr
    start = time.time()
    for epoch in range(pars.sn):
        net.train()
        for i, (images, labels) in enumerate(train_loader):
            images = Variable(images).cuda() if CUDA_EXISTS else Variable(images)
            labels = Variable(labels).cuda() if CUDA_EXISTS else Variable(labels)
            current_loss = criterion(net(images), labels)
            sampler.zero_grad()
            current_loss.backward()
            sampler.step()

        """ Adjust the learning rate before warm-ups """
        if pars.model == 'resnet' and epoch in [int(0.7*pars.sn), int(0.9*pars.sn)]:
            cur_lr /= pars.lr_gap
            print('Learning rate {:.4f}'.format(cur_lr))
        elif pars.model != 'resnet' and epoch <= pars.warm * pars.sn:
            cur_beta = epoch * 1.0 / (pars.warm * pars.sn)
            cur_lr = 0.1 / 2 * (np.cos(np.pi * min(cur_beta, 0.9)) + 1)

        for group in sampler.param_groups:
            group['lr'] = cur_lr

        """ Report results """
        if epoch < int(0.75*pars.warm*pars.sn):
            BMA.eval(pars.data, net, test_loader, criterion, bma=False, uq=False)
        else:
            BMA.eval(pars.data, net, test_loader, criterion, bma=True, uq=False)
        print('Epoch {} lr: {:.4f} Acc: {:0.2f} BMA: {:0.2f} Best Acc: {:0.2f} Best BMA: {:0.2f}'.format(\
                epoch, cur_lr, BMA.cur_acc, BMA.bma_acc, BMA.best_cur_acc, BMA.best_bma_acc))

    os.system('mkdir -p ' + './output/checkpoints_' + pars.model + str(pars.depth))
    torch.save(net.state_dict(), './output/checkpoints_' + pars.model + str(pars.depth) + '/model_seed_' + str(pars.seed))
    end = time.time()
    print('Time used {:.2f}s'.format(end - start))
    
    

if __name__ == "__main__":
    main()
