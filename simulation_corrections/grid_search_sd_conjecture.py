#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(5):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([0])
    window = secure_random.choice([300, 300, 3000, 3000, 100, 100, 30, 30, 10, 10, 3, 3, 1])
    if window == 1:
        correction = 0
    elif window == 3:
        correction = secure_random.choice([0, 0.7, 0.8, 0.9, 1.0, 1.1])
    elif window == 10:
        correction = secure_random.choice([0, 1.8, 1.9, 2.0, 2.1])
    elif window == 30:
        correction = secure_random.choice([0, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3])
    elif window == 100:
        correction = secure_random.choice([0, 4.1, 4.2, 4.3, 4.4, 4.5])
    elif window == 300:
        correction = secure_random.choice([0, 5.2, 5.3])
    elif window == 1000:
        correction = secure_random.choice([0, 6.4, 6.5, 6.6, 6.7])
    elif window == 3000:
        correction = secure_random.choice([0, 6.9, 7.0, 7.1, 7.2, 7.3])
    #correction = 0
    lr = 0.01
    os.system(f'/usr/bin/Rscript sample_code_high_t_4.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_high_tau_4_seed_{seed}')
