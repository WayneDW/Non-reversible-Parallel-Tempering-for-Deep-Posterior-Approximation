#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(20):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([6])
    window = secure_random.choice([1, 3, 10, 30, 100, 300, 1000, 3, 10, 30, 100, 300, 1000, 3000, 3000])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0.2, 0.3, 0.4, 0.5])
    elif window == 10:
        correction = secure_random.choice([0.3, 0.4, 0.5, 0.6])
    elif window == 30:
        correction = secure_random.choice([0.4, 0.5, 0.6, 0.7])
    elif window == 100:
        correction = secure_random.choice([0.5, 0.6, 0.7, 0.8])
    elif window == 300:
        correction = secure_random.choice([0.6, 0.7, 0.8, 0.9, 1.0, 1.1])
    elif window == 1000:
        correction = secure_random.choice([1.6, 1.8, 2.0, 2.2, 2.4, 2.6])
    elif window == 3000:
        correction = secure_random.choice([1.6, 1.8, 2.0, 2.2, 2.4, 2.6])
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_no_DEO_seed_{seed}')
