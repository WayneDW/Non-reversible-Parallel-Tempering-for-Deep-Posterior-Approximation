#!/usr/bin/env python3
import random
import os
import time
import sys

secure_random = random.SystemRandom()


for _ in range(1):
    seed = str(random.randint(1, 10**5))
    sd = secure_random.choice([4])
    window = secure_random.choice([3])
    correction = secure_random.choice([2.0, 2.1, 2.2, 2.3, 2.4, 2.5])
    

    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
