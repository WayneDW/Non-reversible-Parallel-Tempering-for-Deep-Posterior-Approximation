#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(5):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([7])
    window = secure_random.choice([1, 3, 10, 30, 100, 300, 1000, 3000])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0])
    elif window == 10:
        correction = secure_random.choice([0])
    elif window == 30:
        correction = secure_random.choice([0])
    elif window == 100:
        correction = secure_random.choice([0])
    elif window == 300:
        correction = secure_random.choice([0])
    elif window == 1000:
        correction = secure_random.choice([0])
    elif window == 3000:
        correction = secure_random.choice([0])
    lr = 0.005
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO_sd_7.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_sd_7_seed_{seed}')
