# coding: UTF-8
#ランダムに決めようという試み
import random
r = [2,45,4,5,6,9]
ran = random.randint(0, len(r))
yy = random.sample(r, ran)
print(yy)

#101*101のフィールドを作った
import numpy as np
deka = 101
baio = np.zeros((deka, deka))
baio[int((deka - 1) / 2), int((deka - 1) / 2)]

#ランダムで分裂する奴をマイナスにする
for i in range(0, 101):
    for j in range(0, 101):
        if baio[i][j] != 0:
            bunretu = np.random.choice(["do", "dont"], p=[0.5, 0.5])
            if bunretu == "do":
                baio[i][j] = baio[i][j] * -1
            else:
                pass

#螺旋のループ
ba = np.zeros((5,5))

for r in range(0, 3):
    for k in range(0, 2 * r):
        ba[2 - r, 2 - r + k] = 1
        ba[2 - r + k, 2 + r] = 2
        ba[2 + r, 2 + r - k] = 3
        ba[2 + r - k, 2 - r] = 4
