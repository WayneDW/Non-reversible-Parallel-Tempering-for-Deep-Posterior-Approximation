#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(2):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([0])
    window = secure_random.choice([3, 10, 30, 100, 300, 1000, 3000])
    #window = 1
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0.9])
    elif window == 10:
        correction = secure_random.choice([2.2])
    elif window == 30:
        correction = secure_random.choice([3.5])
    elif window == 100:
        correction = secure_random.choice([4.9])
    elif window == 300:
        correction = secure_random.choice([6.1])
    elif window == 1000:
        correction = secure_random.choice([7.5])
    elif window == 3000:
        correction = secure_random.choice([8.8])
    #correction = 0
    lr = 0.01
    print(f'/usr/bin/Rscript sample_code_high_t_5.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_high_tau_5_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_high_t_5.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_high_tau_5_seed_{seed}')
