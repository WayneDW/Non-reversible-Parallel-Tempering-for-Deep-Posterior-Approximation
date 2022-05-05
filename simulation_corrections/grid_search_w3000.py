#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(10):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([0, 2, 3, 4, 5])
    window = 3000

    if sd == 5:
        correction = secure_random.choice([2.4, 2.6, 3.2, 3.4, 3.5, 3.7, 3.8])
    elif sd == 4:
        correction = secure_random.choice([5.1, 5.3, 5.5])
    elif sd == 3:
        correction = secure_random.choice([6.1, 6.3, 6.5, 6.7])
    elif sd == 2:
        correction = secure_random.choice([6.4, 6.45, 6.5, 6.55, 6.6])
    elif sd == 0:
        correction = secure_random.choice([6.85, 6.9, 6.95])
    #correction = 0
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
