# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt

t = 0.0
h = 0.01

a = float(input("被食者の増殖率:"))
b = float(input("被食者の被食率:"))
c = float(input("捕食者の増殖率:"))
d = float(input("捕食者の補食率:"))
x = float(input("捕食者の初期数:"))
y = float(input("被食者の初期数:"))

tlist = [t]
xlist = [x]
ylist = [y]

while t <= 100:
    t += h
    dx = a * x - b * x * y
    dy = c * x * y - d * y
    x += dx * h
    y += dy * h
    print("{:.1} {:.1}".format(t,x))
    print("{:.1} {:.1}".format(t,y))

    tlist.append(t)
    xlist.append(x)
    ylist.append(y)

plt.plot(tlist,xlist)
plt.plot(tlist,ylist)
plt.show()
