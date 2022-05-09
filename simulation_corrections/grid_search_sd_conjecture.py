#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(5):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([0])
    window = secure_random.choice([3, 10, 30, 100, 300, 1000, 3000])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0.4, 0.5, 0.6])
    elif window == 10:
        correction = secure_random.choice([1.3, 1.4, 1.5, 1.6])
    elif window == 30:
        correction = secure_random.choice([2.2, 2.3, 2.4, 2.5])
    elif window == 100:
        correction = secure_random.choice([3.4, 3.5, 3.6, 3.7])
    elif window == 300:
        correction = secure_random.choice([4.4, 4.5, 4.6, 4.7, 4.8, 4.9])
    elif window == 1000:
        correction = secure_random.choice([5.4, 5.5, 5.6, 5.7, 5.8, 5.9])
    elif window == 3000:
        correction = secure_random.choice([6.4, 6.5, 6.6, 6.7, 6.8, 6.9])
    lr = 0.01
    os.system(f'/usr/bin/Rscript sample_code_high_t_20.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_high_tau_20_seed_{seed}')
