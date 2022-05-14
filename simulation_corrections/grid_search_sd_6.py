#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(2):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([6])
    window = secure_random.choice([1000])
    if window == 1:
        correction = 0 # 3.97e-2
    elif window == 3:
        correction = secure_random.choice([0.3]) # 28/ 3.30e-2 
    elif window == 10:
        correction = secure_random.choice([0.4]) # 16/ 3.67e-2
    elif window == 30:
        correction = secure_random.choice([0.5]) # 16/ 3.31e-2
    elif window == 100:
        correction = secure_random.choice([0.6]) # _1.1_no_DEO cnt 11 MAE  3.59e-02
    elif window == 300:
        correction = secure_random.choice([0.65, 0.90])
    elif window == 1000:
        correction = secure_random.choice([0.95])
    elif window == 3000:
        correction = secure_random.choice([1.15])
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_no_DEO_seed_{seed}')
