#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(10):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([3])
    window = secure_random.choice([3, 10, 30, 100, 300, 1000])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([1])
    elif window == 10:
        correction = secure_random.choice([1.5])
    elif window == 30:
        correction = secure_random.choice([2.3])
    elif window == 100:
        correction = secure_random.choice([3.3])
    elif window == 300:
        correction = secure_random.choice([4.4])
    elif window == 1000:
        correction = secure_random.choice([5.4])
    correction = 0
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
