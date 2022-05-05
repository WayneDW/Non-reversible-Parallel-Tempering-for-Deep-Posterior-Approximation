#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(15):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([2, 3, 4, 5])
    window = 3000

    if sd == 5:
        correction = secure_random.choice([3.0, 3.3, 3.6, 3.9, 4.2, 4.5])
    elif sd == 4:
        correction = secure_random.choice([4.8, 5.0, 5.2, 5.4, 5.6])
    elif sd == 3:
        correction = secure_random.choice([6.0, 6.2, 6.4, 6.6, 6.8])
    elif sd == 2:
        correction = secure_random.choice([6.6, 6.8, 7, 7.2, 7.4])
    elif sd == 0:
        correction = secure_random.choice([6.6, 6.8, 7, 7.2, 7.4])
    correction = 0
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
