#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(1):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([0])
    window = secure_random.choice([1, 2, 3, 10, 30, 100, 300, 1000, 3000])
    window = 3
    if window == 1:
        correction = 0
    elif window == 2:
        correction = secure_random.choice([0.07])
    elif window == 3:
        correction = secure_random.choice([0.07, 0.08, 0.09, 0.1])
    elif window == 10:
        correction = secure_random.choice([0.45, 0.46, 0.47, 0.48, 0.49])
    elif window == 30:
        correction = secure_random.choice([0.47, 0.48, 0.49, 0.50])
    elif window == 100:
        correction = secure_random.choice([0.48, 0.49, 0.50, 0.51, 0.52])
    elif window == 300:
        correction = secure_random.choice([0.50, 0.51, 0.52, 0.53, 0.54, 0.56, 0.58, 0.60])
    elif window == 1000:
        correction = secure_random.choice([0.56, 0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70])
    elif window == 3000:
        correction = secure_random.choice([0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74])
    sd_proposal = secure_random.choice([2])
    os.system(f'/usr/bin/Rscript sample_code_MH.r {sd} {window} {correction} {seed} {sd_proposal} > output/output_sd_proposal_{sd_proposal}_sd_{sd}_window_{window}_corr_{correction}_MH_seed_{seed}')
