# coding: UTF-8
import numpy as np
bunretu = np.random.choice(["do", "dont"], p=[0.5, 0.5])
print(bunretu)

ba = np.zeros((5,5))

for r in range(0, 3):
    for k in range(0, 2 * r):
        ba[2 - r, 2 - r + k] = 1
        ba[2 - r + k, 2 + r] = 2
        ba[2 + r, 2 + r - k] = 3
        ba[2 + r - k, 2 - r] = 4
print(ba)
