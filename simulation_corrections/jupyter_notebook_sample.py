#!/usr/bin/env python3

import sys
import autograd.numpy as np
from autograd import grad
#from autograd.scipy.stats import norm
from scipy.stats import norm
from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import rcParams

from tqdm import tqdm


num_samples = int(sys.argv[1])

def gaussian_density(x, mean, sd):
    return 1. / sd / np.sqrt(2 * np.pi) * np.exp(-0.5 * (x-mean)**2 / sd**2)

def gaussian_mixture_density(x):
    return 0.4 * gaussian_density(x, -4, 0.7) + 0.6 * gaussian_density(x, 3, 0.5)

def energy_function(x):
    return -np.log(gaussian_mixture_density(x))

energy_gradient = grad(energy_function)

def noisy_energy(x, std): return energy_function(x) + norm.rvs(size=1, loc=0, scale=std)

class PT_sampler:
    def __init__(self, lr=0.01, window=1, w_correction=0, std=0, T=[1, 10], num_samples=100000):
        self.lr = lr
        self.T_low, self.T_high = T
        self.x_low, self.x_high = 0., 0.
        self.num_samples, self.thinning = num_samples, 10
        
        self.window, self.w_correction = window, w_correction
        self.std = std
        
        self.swaps, self.gate = 0, 1
        print(f'lr {lr} window {window} w-correction {w_correction} sd of energy {std}')
        self._solver()
        
    def _solver(self):
        self.samples = []
        scale_low, scale_high = np.sqrt(2 * self.lr * self.T_low), np.sqrt(2 * self.lr * self.T_high)
        delta_invT = 1 / self.T_high - 1 / self.T_low
        
        for counter in tqdm(range(int(self.num_samples*self.thinning*1.2)), miniters=1000):
            """ open the gate """
            if counter % self.window == 0:
                gate = 1
            
            """ parallel samplers with different temperatures """
            self.x_low += -self.lr * energy_gradient(self.x_low) + norm.rvs(scale=scale_low)
            self.x_high += -self.lr * energy_gradient(self.x_high) + norm.rvs(scale=scale_high)
            
            
            """ compute swap rate """
            delta_energy = noisy_energy(self.x_high, self.std) - noisy_energy(self.x_low, self.std)
            
            swap_rate = min(1, np.exp(delta_invT * (delta_energy - delta_invT * self.std**2) - self.w_correction))
            
            """ swap and close the gate """
            if np.random.uniform(low=0, high=1) < swap_rate and gate == 1:
                self.x_low, self.x_high = self.x_high, self.x_low
                self.swaps += 1
                self.gate = 0
            
            if counter % self.thinning == 0:
                self.samples.append(self.x_low)
        
        """ remove burn-in steps """
        self.samples = self.samples[-num_samples: ]

sampler_PT = PT_sampler(window=1, w_correction=0, std=0, num_samples=num_samples)

sampler_PT_100_38_0 = PT_sampler(window=100, w_correction=3.8, std=0, num_samples=num_samples)
sampler_PT_100_33_0 = PT_sampler(window=100, w_correction=3.3, std=0, num_samples=num_samples)
sampler_PT_100_28_0 = PT_sampler(window=100, w_correction=2.8, std=0, num_samples=num_samples)


real_samples = norm.rvs(size=int(num_samples*0.4), loc=-4, scale=0.7).tolist() + \
               norm.rvs(size=int(num_samples*0.6), loc=3, scale=0.5).tolist()

x_ticks = np.arange(-6, 5, 0.1)

MAE = np.mean(np.abs(gaussian_kde(real_samples)(x_ticks) - gaussian_kde(sampler_PT.samples)(x_ticks)))
print(f'MAE {MAE: .2e}')

MAE = np.mean(np.abs(gaussian_kde(real_samples)(x_ticks) - gaussian_kde(sampler_PT_100_38_0.samples)(x_ticks)))
print(f'MAE {MAE: .2e}')

MAE = np.mean(np.abs(gaussian_kde(real_samples)(x_ticks) - gaussian_kde(sampler_PT_100_33_0.samples)(x_ticks)))
print(f'MAE {MAE: .2e}')

MAE = np.mean(np.abs(gaussian_kde(real_samples)(x_ticks) - gaussian_kde(sampler_PT_100_28_0.samples)(x_ticks)))
print(f'MAE {MAE: .2e}')
