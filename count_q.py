from pylab import loadtxt
import math
import numpy as np
import matplotlib.pyplot as plt

data = loadtxt('processed_data.txt', usecols=(
    0, 1, 2, 3), skiprows=0, unpack=True)
# load filename, take columns 0 & 1 & 2 & 3, skip 1 row, unpack=transpose x&y


def calculate_Q(a, n, X, Y):
    plt.figure()
    plt.plot(X, Y)
    stop = a * math.exp(-math.pi/n)
    plt.title(f'a = {a}, n = {n}, stop = {stop}')
    plt.axhline(stop, color='black')
    
    stoptime = None
    for i in range(len(Y)):
        if max(Y[i:]) <= stop:
            stoptime = X[i]
            return (n*(stoptime/T))


xdata = data[0]
ydata = data[1]

s = 0
n = len(xdata)

X = xdata[s:n]
Y = ydata[s:n]

n = len(X)
a = 0.4522

T = 1.6372109484448187
# plt.axhline(abs(Y[0]) * math.exp(-math.pi/2), color='black')
# plt.show()
Q = []
for n in range(1, 10):
    q = calculate_Q(a, n, X, Y)
    Q.append(q)
    print(f"{n} & {int(q)}\\\\")
# plt.show()
print(np.mean(Q))
