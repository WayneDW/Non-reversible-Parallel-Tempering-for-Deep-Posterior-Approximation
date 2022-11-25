"""
Code for Non-reversible Parallel Tempering for Deep Posterior Approximation
(c) Wei Deng
Nov 24, 2022
"""

#!/usr/bin/python

import math
import copy
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
import torch.nn as nn
import torch.nn.parallel
from torchvision import datasets, transforms
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
import torch.utils.data as data
import torchvision.datasets as datasets

import models.cifar as cifar_models
from models.cifar import PyramidNet as PYRM

from tools import loader
from trainer import trainer, trainer_vanilla_ensemble, trainer_cyc_ensemble

def main():
    parser = argparse.ArgumentParser(description='Grid search')
    parser.add_argument('-type', default='PT', type=str, help='[PT] or [vanilla] ensemble or [cyclic]')
    parser.add_argument('-aug', default=1, type=float, help='Data augmentation or not')
    """ numper of optimization/ sampling epochs """
    parser.add_argument('-sn', default=500, type=int, help='Sampling Epochs')
    parser.add_argument('-wdecay', default=5e-4, type=float, help='Samling weight decay')
    parser.add_argument('-lr_max', default=0.02, type=float, help='Sampling learning rate')
    parser.add_argument('-lr_min', default=0.005, type=float, help='Sampling learning rate')
    parser.add_argument('-momentum', default=0.9, type=float, help='Sampling momentum learning rate')

    """ data, model and batch size """
    parser.add_argument('-data', default='cifar100', dest='data', help='CIFAR10')
    parser.add_argument('-total', default=50000, type=int, help='total data points')
    parser.add_argument('-model', default='resnet', type=str, help='resnet')
    parser.add_argument('-depth', type=int, default=20, help='Model depth.')
    parser.add_argument('-batch', default=256, type=int, help='Batch size')

    """ Parallel Tempering hyperparameters """
    parser.add_argument('-chains', default=10, type=int, help='Total number of chains')
    parser.add_argument('-swap_rate', default=5e-3, type=float, help='target swapping rate')
    parser.add_argument('-window_custom', default=0, type=int, help='customized window size (0 -> optimal)')
    parser.add_argument('-correction', default=0.1, type=float, help='initial correction')
    parser.add_argument('-gamma', default=600.0, type=float, help='smoothiing factor')
    parser.add_argument('-scale', default=10.0, type=float, help='scale factor')

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
    nets = []
    for idx in range(pars.chains):
        if pars.model == 'resnet':
            if pars.data == 'cifar10':
                net = cifar_models.__dict__['resnet'](num_classes=10, depth=pars.depth).cuda()
            elif pars.data == 'cifar100':
                net = cifar_models.__dict__['resnet'](num_classes=100, depth=pars.depth).cuda()

        nets.append(pickle.loads(pickle.dumps(net)))

    """ Step 2: Load Data """
    train_loader, test_loader = loader(pars.batch, pars.batch, pars)

    PATH = './output/checkpoints_' + pars.model + str(pars.depth) + '/'
    candidate_models = os.listdir(PATH)
    selected_models = np.random.choice(candidate_models, size=pars.chains)

    for idx in range(pars.chains):
        print('Pick {}'.format(selected_models[idx]))
        nets[idx].load_state_dict(torch.load(PATH + selected_models[idx], map_location='cuda:' + str(pars.gpu)))

    """ Step 4: Bayesian Sampling """
    if pars.type == 'vanilla':
        trainer_vanilla_ensemble(nets, train_loader, test_loader, pars)
    elif pars.type == 'cyc':
        trainer_cyc_ensemble(nets, train_loader, test_loader, pars)
    else:
        trainer(nets, train_loader, test_loader, pars)
    
    

if __name__ == "__main__":
    main()
