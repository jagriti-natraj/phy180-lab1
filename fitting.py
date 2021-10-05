# -*- coding: utf-8 -*-
"""
This program imports data from the file specified by the string filename
The first line of the file is ignored (assuming it's the name of the variables)
After that the data file needs to be formatted: 
number space number space number space number newline
Do NOT put commas in your data file!!
The data file should be in the same directory as this python file
The data should be in the order:
x_data y_data x_uncertainty y_uncertainty

Then this program tries to fit a function to the data points
It plots the data as dots with errorbars and the best fit line
It then prints the best fit information
After that, it plots the "residuals": ydata - fittedfunction(xdata)
That is it subtracts your fitted ideal values from your actual data to see 
what is "left over" from the fit
Ideally your residuals graph should look like noise, otherwise there is more
information you could extract from your data (or you used the wrong fitting
function)

If you want to change the file name, that's the next line below this comment
"""

from pylab import loadtxt
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy.optimize as optimize
filename = "processed_data.txt"
# change this if your filename is different


data = loadtxt(filename, usecols=(0, 1, 2, 3), skiprows=0, unpack=True)
# load filename, take columns 0 & 1 & 2 & 3, skip 1 row, unpack=transpose x&y

xdata = data[0]
ydata = data[1]
xerror = data[2]
yerror = data[3]

s = 0
# s = 0
# n= min([i for i, x in enumerate(xdata) if x >= 30])
n = 0 * len(xdata) + 1*len(xdata)//7
# n = 1000
xdata = xdata[s:n]
ydata = ydata[s:n]
ydata = ydata - np.mean(ydata)
xerror = xerror[s:n]
yerror = yerror[s:n]
# finished importing data, naming it sensibly


def my_func(t, a, tau, T, phi):
    return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)


def my_func_2(t, tau):
    return 0.4709016018612959*np.exp(-t/tau)*np.cos(2*np.pi*t/1.6488407949723451-3.5481978472751607)


def calc_T_from_local_maxima(xdata, ydata):
    maxima = []
    for i in range(5, len(ydata) - 5):
        if non_decreasing(sorted(ydata[i-5:i])) and non_increasing(sorted(ydata[i:i+5])):
            maxima.append(xdata[i])
    return np.mean([x - y for x, y in zip(maxima, maxima[1:])])

# def my_func_2(t,a,tau):
#     return a*np.exp(-t/tau)*np.cos(2*np.pi*t/1.6+math.pi)
# this is the function we want to fit. the first variable must be the
# x-data (time), the rest are the unknown constants we want to determine


init_guess = (0.4709016018612959, 130, 1.6488407949723451, -3.5481978472751607)
init_guess_2 = (130)
# print("T")
# init_guess=(130, 1.7)
# your initial guess of (a,tau,T,phi)

popt, pcov = optimize.curve_fit(
    my_func, xdata, ydata, p0=init_guess, maxfev=10000)
# we have the best fit values in popt[], while pcov[] tells us the uncertainties

a = popt[0]
tau = popt[1]
T = popt[2]
phi = popt[3]

# a, tau, T, phi = init_guess
# tau = popt[0]

# best fit values are named nicely
u_a = pcov[0, 0]**(0.5)
u_tau = pcov[1, 1]**(0.5)
u_T = pcov[2, 2]**(0.5)
u_phi = pcov[3, 3]**(0.5)

# uncertainties of fit are named nicely


def fitfunction(t):
    return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)
# fitfunction(t) gives you your ideal fitted function, i.e. the line of best fit


start = min(xdata)
stop = max(xdata)
# xs=np.arange(start,stop,(stop-start)/200) # fit line has 1000 points
curve = fitfunction(xdata)
# (xs,curve) is the line of best fit for the data in (xdata,ydata)

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.subplots_adjust(hspace=0.6)
# hspace is horizontal space between the graphs

ax1.errorbar(xdata,ydata,yerr=yerror,xerr=xerror,fmt=".", elinewidth=0.2, ms=2)
# ax1.scatter(xdata, ydata, s=2)
# plot the data, fmt makes it data points not a line
ax1.plot(xdata, curve, color='pink')
# plot the best fit curve on top of the data points as a line

ax1.set_xlabel("xdata")
ax1.set_ylabel("ydata")
ax1.set_title("Best fit of some data points")
# HERE is where you change how your graph is labelled

Q = math.pi * tau / T
u_Q = Q*(u_tau/tau + u_T/T)

print(f"Amplitude $(a)$ & ${a} \pm {u_a}$\\\\")
print(f"Tau $(\\tau)$ & ${tau} \pm {u_tau}$\\\\")
print(f"Time Period $(T)$ & ${T} \pm {u_T}$\\\\")
print(f"Phi $(\phi)$ & ${phi} \pm {u_phi}$\\\\")
print(f"Q-value & ${Q} \pm {u_Q}$\\\\")
# prints the various values with uncertainties

residual = ydata-fitfunction(xdata)
# find the residuals
zeroliney = [0, 0]
zerolinex = [start, stop]
# create the line y=0

ax2.errorbar(xdata,residual,yerr=yerror,xerr=xerror,fmt=".", elinewidth=0.2, ms=2)
# ax2.scatter(xdata, residual, s=2)
# plot the residuals with error bars
ax2.plot(zerolinex, zeroliney)
# plotnthe y=0 line on top

ax2.set_xlabel("xdata")
ax2.set_ylabel("residuals of ydata")
ax2.set_title("Residuals of the fit")
# HERE is where you change how your graph is labelled

plt.show()
# show the graph
