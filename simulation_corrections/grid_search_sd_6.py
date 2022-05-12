#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(1):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([6])
    window = secure_random.choice([100])
    if window == 1:
        correction = 0 # 3.97e-2
    elif window == 3:
        correction = secure_random.choice([0.3]) # 28/ 3.30e-2 
    elif window == 10:
        correction = secure_random.choice([0.4]) # 16/ 3.67e-2
    elif window == 30:
        correction = secure_random.choice([0.5]) # 16/ 3.31e-2
    elif window == 100:
        correction = secure_random.choice([0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.20, 1.25, 1.30, 1.35, 1.4]) # 25/ 4.58e-2
    elif window == 300:
        correction = secure_random.choice([0.7]) # 23/ 4.28e-2
    elif window == 1000:
        correction = secure_random.choice([1.6]) # 12/ 3.93e-2
    elif window == 3000:
        correction = secure_random.choice([1.7]) # 8/ 4.43e-2
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_no_DEO_seed_{seed}')
