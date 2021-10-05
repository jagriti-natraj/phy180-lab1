import scipy.optimize as optimize
import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import loadtxt

data=loadtxt('processed_data.txt', usecols=(0,1,2,3), skiprows=0, unpack=True)
xdata=data[0]
ydata=data[1]
xerror=data[2]
yerror=data[3]

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))

def monotonic(L):
    return non_increasing(L) or non_decreasing(L)


def calc_T_from_local_maxima(xdata, ydata):
    maxima = []
    res = 2
    for i in range(res, len(ydata) - res):
        if strictly_increasing(sorted(ydata[i-res:i])) and strictly_decreasing(sorted(ydata[i:i+res])):
            maxima.append(xdata[i])
            print(xdata[i])
    return np.mean([x - y for x, y in zip(maxima, maxima[1:])])

print(calc_T_from_local_maxima(xdata, ydata))