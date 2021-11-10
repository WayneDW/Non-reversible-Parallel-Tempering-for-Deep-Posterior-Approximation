"""
Code for Non-reversible Parallel Tempering for Uncertainty Approximation
(c) Anonymous authors
Nov 8, 2021
"""

#!/usr/bin/python 
import random 
import os
import time
import sys

import numpy as np
 
secure_random = random.SystemRandom()


if len(sys.argv) == 2:
    gpu = sys.argv[1]
elif len(sys.argv) > 2:
    sys.exit('Unknown input')
else:
    gpu = '0'

#os.system('sleep 1h')

for _ in range(1):
    seed = str(random.randint(1, 10**5))
    batch, data = secure_random.choice([('256', 'cifar100')])
    '''
    """ Initialize models """
    sn, model, depth = secure_random.choice([('1000', 'resnet', '20')])
    os.system('python bayes_init.py -sn ' + sn + ' -data ' + data + ' -model ' + model + ' -depth ' + depth + ' -gpu ' + gpu + ' > ./output/' + data + '_' + model + depth + '_sn_' + sn + '_batch_' + batch + '_v5_seed_' + seed)
    '''

    
    """ Parallel tempering on optimized paths """
    types = secure_random.choice(['PT'])
    sn, model, depth = secure_random.choice([('500', 'resnet', '20')])
    chains = '10'
    gamma = secure_random.choice(['600'])
    scale =  secure_random.choice(['10'])
    correction = secure_random.choice(['0.1'])
    swap_rate = secure_random.choice(['5e-3'])
    window = secure_random.choice(['1'])
    if window == '0':
        """ direct 0 to the optimal """
        window = str(int(np.ceil((np.log(int(chains)) + np.log(np.log(int(chains)))) / -np.log(1 - float(swap_rate)))))


    lr_max, lr_min = secure_random.choice([('0.02', '0.005')])
    os.system('python bayes_cnn.py -sn ' + sn + ' -type ' + types + ' -data ' + data + ' -model ' + model + ' -depth ' + depth + ' -batch ' + batch + ' -chains ' + chains \
            + ' -lr_min ' + lr_min + ' -lr_max ' + lr_max + ' -correction ' + correction + ' -gamma ' + gamma + ' -scale ' + scale + ' -swap_rate ' + swap_rate + ' -window_custom ' + window + ' -gpu ' + gpu \
            + ' > ./output/' + types + '_' + data + '_' + model + depth + '_sn_' + sn + '_batch_' + batch + '_chain_' + chains + '_lr_min_max_' + lr_min + '_' + lr_max + '_correction_' + correction + '_gamma_' + gamma + '_r_' + swap_rate + '_wd_' + window + '_scale_' + scale + '_pretrain_sn_300_final_seed_' + seed)
