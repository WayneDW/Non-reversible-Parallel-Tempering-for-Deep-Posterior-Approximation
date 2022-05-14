#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(10):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([7])
    window = secure_random.choice([3, 10, 30, 100])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    elif window == 10:
        correction = secure_random.choice([0.10, 0.15, 0.20, 0.25, 0.30, 0.35])
    elif window == 30:
        correction = secure_random.choice([0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45])
    elif window == 100:
        correction = secure_random.choice([0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55])
    elif window == 300:
        correction = secure_random.choice([0.65, 0.90])
    elif window == 1000:
        correction = secure_random.choice([0.95])
    elif window == 3000:
        correction = secure_random.choice([1.15])
    lr = 0.005
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO_sd_7.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_sd_7_seed_{seed}')
