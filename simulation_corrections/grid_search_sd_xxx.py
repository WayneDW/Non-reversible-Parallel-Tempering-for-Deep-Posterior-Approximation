#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(10):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([0])#, 2, 3, 4, 5, 4, 3, 2, 4, 3, 2, 0])
    window = secure_random.choice([3])
    if sd == 0:
        correction = secure_random.choice([0.55, 0.65, 0.65, 0.7, 0.75, 0.8, 0.85])
    elif sd == 2:
        correction = secure_random.choice([0.55, 0.65, 0.75, 0.9])
    elif sd == 3:
        correction = secure_random.choice([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    elif sd == 4:
        correction = secure_random.choice([1.35, 1.4, 1.45])
    elif sd == 5:
        correction = secure_random.choice([0.05])
    #correction = 0
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
