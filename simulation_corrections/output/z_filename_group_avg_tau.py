#!/usr/bin/env python3

import os, sys, re
from glob import glob


group_to_mae = {}
group_to_swaps = {}
cnt_to_mae = {}
for filename in glob('./output*sd*tau_4*'):
    num_swaps, mae = 0, 0
    for line in open(filename):
        line = line.strip()
        #m = re.match(r'\"Number of swaps\" \"(\d+)\"', line)
        m = re.match(r'.*Number of swaps" "(.+)"', line)
        if m:
            num_swaps = int(m.group(1))

        m = re.match(r'.*Sum of error"(.+)"(.+)"', line)
        if m:
            mae = float(m.group(2))

        if num_swaps > 0 and mae > 0:
            #output_sd_4_window_1_corr_0_seed_2537_swap_30182_MAE_0.034801212762021_end
            m = re.match(r'.*sd_(.+)_window_(.+)_corr_(.+)_seed_(.+).*', filename)
            sd = m.group(1)
            window = m.group(2)
            corr = m.group(3)
            feat = f'sd_{sd}_window_{window}_corr_{corr}'
            if feat not in group_to_mae:
                group_to_mae[feat], cnt_to_mae[feat] = 0, 0
                group_to_swaps[feat] = 0
            group_to_mae[feat] += mae
            group_to_swaps[feat] += num_swaps
            cnt_to_mae[feat] += 1

for feat in sorted(cnt_to_mae.keys()):
    cnt = cnt_to_mae[feat]
    mae_avg = group_to_mae[feat] / cnt_to_mae[feat]
    swaps_avg = group_to_swaps[feat] * 1.0 / cnt_to_mae[feat]
    print(f'{feat} cnt {cnt} MAE {mae_avg: .2e} Swaps {swaps_avg: .1f}')

    
