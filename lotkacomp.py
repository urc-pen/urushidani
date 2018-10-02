# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt

t = 0.0
h = 0.01

r1 = float(input("1の内的増加率?:"))
r2 = float(input("2の内的増加率?:"))
N1 = float(input("1の初期数?:"))
N2 = float(input("2の初期数?:"))
a12 = float(input("1の競争係数?:"))
a21 = float(input("2の競争係数?:"))
K1 = float(input("1の環境収容力?:"))
K2 = float(input("2の環境収容力?:"))

tlist = [t]
N1list = [N1]
N2list = [N2]

while t <= 100:
    t += h
    dN1 = r1 * N1 * (1 - (N1 + a12 * N2) / K1)
    dN2 = r2 * N2 * (1 - (N2 + a21 * N1) / K2)
    N1 += dN1 * h
    N2 += dN2 * h
    print("{:.5} {:.5}".format(t,N1))
    print("{:.5} {:.5}".format(t,N2))

    tlist.append(t)
    N1list.append(N1)
    N2list.append(N2)

plt.plot(tlist,N1list)
plt.plot(tlist,N2list)
plt.show()
