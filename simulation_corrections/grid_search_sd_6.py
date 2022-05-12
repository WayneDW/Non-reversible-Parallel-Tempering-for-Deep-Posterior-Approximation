#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(5):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([6])
    window = secure_random.choice([100, 1000, 3000])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0.3])
    elif window == 10:
        correction = secure_random.choice([0.4])
    elif window == 30:
        correction = secure_random.choice([0.5])
    elif window == 100:
        correction = secure_random.choice([0.45, 0.55, 0.65, 0.75, 0.85])
    elif window == 300:
        correction = secure_random.choice([0.7])
    elif window == 1000:
        correction = secure_random.choice([1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
    elif window == 3000:
        correction = secure_random.choice([1.3, 1.4, 1.5, 1.7, 1.9, 2.1])
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_no_DEO_seed_{seed}')
