# Non-reversible Parallel Tempering for Deep Posterior Approximation

A user-friendly parallel tempering algorithm that tracks the non-reversibility property with an optimal round trip time in deep learning. We adopt stochastic gradient descent (SGD) with large and constant learning rates as user-friendly exploration kernels.

```
@inproceedings{NTPT_big_data,
  title={Non-reversible Parallel Tempering for Deep Posterior Approximation},
  author={Wei Deng and Qian Zhang and Qi Feng and Faming Liang and Guang Lin},
  booktitle={Thirty-Seventh AAAI Conference on Artificial Intelligence (AAAI'23)},
  year={2023}
}
```

### Requirement
* Python 2.7
* [PyTorch = 1.1](https://pytorch.org/) or similar
* numpy
* CUDA 



## Uncertainty Estimation and Optimization on CIFAR100: ResNet20 with batch size 256


Pretrain models for ensemble (mSGDxP10) and parallel tempering (DEO-mSGD×P10 and DEO star-mSGD×P10)

```python
$ python bayes_init.py -model resnet -depth 20 -sn 300
```

### Run 10 short parallel chains with 500 epochs
Run the standard ensemble (mSGDxP10), i.e. run 10 parallel chains 500 epochs based on momentum SGD
```python
$ python bayes_cnn.py -sn 500 -type vanilla -model resnet -depth 20 -chains 10 -lr_min 0.005
```

Run DEO-mSGD×P10 with a **window size of 1**
```python
$ python bayes_cnn.py -sn 500 -type PT -model resnet -depth 20 -chains 10 -lr_min 0.005 -lr_max 0.02 -swap_rate 5e-3 -window_custom 1
```

Run DEO star-mSGD×P10 based on the **optimal window size of 626**
```python
$ python bayes_cnn.py -sn 500 -type PT -model resnet -depth 20 -chains 10 -lr_min 0.005 -lr_max 0.02 -swap_rate 5e-3 -window_custom 626
```

### Run a long single chain with 5,000 chains

```python
$ python bayes_cnn.py -sn 5000 -type cyc -data cifar100 -depth 20
```

**Remark:** changing the number of depth can easily reproduce the results for ResNet32 and ResNet56 models
