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
        #0.45_no_DEO cnt 13 MAE  4.94e-02 
        #corr_0.5_no_DEO cnt 70 MAE  4.64e-02
        #window_100_corr_0.55_no_DEO cnt 8 MAE  4.78e-02
        #window_100_corr_0.6_no_DEO cnt 25 MAE  4.58e-02
        correction = secure_random.choice([0.6]) # _1.1_no_DEO cnt 11 MAE  3.59e-02
    elif window == 300:
        #0.65_no_DEO cnt 18 MAE  3.91e-02
        #0.7_no_DEO cnt 44 MAE  4.36e-02
        #0.9_no_DEO cnt 21 MAE  3.87e-02 Swaps  481.3
        correction = secure_random.choice([0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
    elif window == 1000:
        #0.8_no_DEO cnt 18 MAE  4.35e-02
        #0.95_no_DEO cnt 25 MAE  4.19e-02
        #1.2_no_DEO cnt 11 MAE  4.36e-02
        #1.6_no_DEO cnt 12 MAE  3.93e-02
        correction = secure_random.choice([1.6, 1.2, 0.95, 0.8])
    elif window == 3000:
        #0.7_no_DEO cnt 20 MAE  4.35e-02
        #0.75_no_DEO cnt 15 MAE  4.40e-02
        #1.5_no_DEO cnt 7 MAE  4.86e-02 Swaps  329.9
        correction = secure_random.choice([0.75])
    lr = 0.01
    #print(f'/usr/bin/Rscript sample_code.r {sd} {window} {correction} {seed} > output/output_sd_{sd}_window_{window}_corr_{correction}_seed_{seed}')
    os.system(f'/usr/bin/Rscript sample_code_no_DEO.r {sd} {window} {correction} {seed} {lr} > output/output_lr_{lr}_sd_{sd}_window_{window}_corr_{correction}_no_DEO_seed_{seed}')
