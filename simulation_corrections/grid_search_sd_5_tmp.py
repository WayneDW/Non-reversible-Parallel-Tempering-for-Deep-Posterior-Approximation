#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(2):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([5])
    window = secure_random.choice([1, 3, 10, 30, 100, 300, 300, 300, 300, 1000])
    window = 1000
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    elif window == 10:
        correction = secure_random.choice([0.8, 1.0, 1.2, 1.4])
    elif window == 30:
        correction = secure_random.choice([0.8, 1.0, 1.2, 1.4, 1.6, 1.8])
    elif window == 100:
        correction = secure_random.choice([0.5, 0.7, 0.9, 1.1, 1.3])
    elif window == 300:
        correction = secure_random.choice([1.0, 1.2, 1.4, 1.6])
    elif window == 1000:
        correction = secure_random.choice([2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3])

    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')