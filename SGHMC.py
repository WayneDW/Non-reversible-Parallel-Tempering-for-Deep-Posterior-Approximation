"""
Code for Non-reversible Parallel Tempering for Deep Posterior Approximation
(c) Wei Deng
Nov 24, 2022

This file is a baseline sampler to run cyclic SG-MCMC
    It is used in the exploitation period of the cyclic SG-MCMC and SWAG algorithms
"""

import sys
import numpy as np
import torch
import random
from torch.autograd import Variable

class SGHMC:
    def __init__(self, net, lr=2e-6, T=0.001):
        self.net = net
        self.lr = lr
        """ cold posterior effect due to data augmentation """
        self.T = T
        self.momentum = 0.9
        self.wdecay = 5e-4 * 50000
        self.V = 0.01
        self.velocity = []
        self.alpha = 1 - self.momentum
        for param in net.parameters():
            p = torch.zeros_like(param.data)
            self.velocity.append(p)
    
    def step(self, x, y):
        beta = 0.5 * self.V * self.lr
        noise_scale = np.sqrt(2.0 * self.lr * (self.alpha - beta)) * np.sqrt(self.T)

        for i, param in enumerate(self.net.parameters()):
            proposal = torch.cuda.FloatTensor(param.data.size()).normal_().mul(noise_scale)
            grads = param.grad.data
            if self.wdecay != 0:
                grads.add_(self.wdecay, param.data)
            self.velocity[i].mul_(self.momentum).add_(-self.lr, grads).add_(proposal)
            param.data.add_(self.velocity[i])
