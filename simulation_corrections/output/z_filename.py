#!/usr/bin/env python3

import os, sys, re
from glob import glob


for filename in glob('./output*'):

    for line in open(filename):
        line = line.strip()
        #m = re.match(r'\"Number of swaps\" \"(\d+)\"', line)
        m = re.match(r'.*Number of swaps" "(.+)"', line)
        if m:
            num_swaps = m.group(1)

        m = re.match(r'.*Sum of error"(.+)"(.+)"', line)
        if m:
            mae = m.group(2)


    print(f'Swaps {num_swaps} MAE {mae}')
    if not filename.endswith('_end'):
        os.system(f'mv {filename} {filename}_swap_{num_swaps}_MAE_{mae}_end')
