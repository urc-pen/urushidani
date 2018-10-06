# coding: UTF-8
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import seaborn as sns
import sys
np.set_printoptions(threshold=np.inf)
#deka*dekaのbaioというフィールドを作って、原点の座標(on,on)＝1と定めた。
deka = 55                   #フィールドの大きさ
baio = np.zeros((deka, deka))
on = int((deka - 1) / 2)
baio[on, on] = -1
t = 0
MAXT = 9                #分裂回数

#ランダムで分裂する奴をマイナスにする関数
def bunretumainasu():
    for i in range(1, deka - 1):
        for j in range(1, deka - 1):
            if baio[i][j] != 0:
                bunretu = np.random.choice(["do", "dont"], p=[1, 0])
                if bunretu == "do":
                    baio[i][j] = baio[i][j] * -1
                else:
                    pass
#マイナスをリセットする関数
def mainasureset():
    for i in range(0, deka):
        for j in range(0, deka):
            if baio[i][j] < 0:
                baio[i][j] = baio[i][j] * -1

#分裂の関数。mi,mjを入れると分裂する
def bunretu(mi,mj):
    itii = motoi + mi
    itij = motoj + mj
    bunretuiti = baio[itii, itij]

    if bunretuiti == 0:
        if motoiti == -1:
            baio[motoi, motoj] = 2
            baio[itii, itij] = 3
        if motoiti == -2:
            baio[motoi, motoj] = 4
            baio[itii, itij] = 5
        if motoiti == -3:
            baio[motoi, motoj] = 6
            baio[itii, itij] = 7
        if motoiti < -3:
            baio[itii, itij] = motoiti * -1
            baio[motoi, motoj] = motoiti * -1

    if bunretuiti != 0:
        while bunretuiti != 0 and itii != 0 and itii != deka - 1 and itij != 0 and itij != deka-1:
            itii += mi
            itij += mj
            bunretuiti = baio[itii, itij]
            if bunretuiti == 0 or itii == 0 or itii == deka - 1 or itij == 0 or itij == deka - 1:
                pass
        while itii != motoi + mi or itij != motoj + mj:
            baio[itii, itij] = baio[itii - mi, itij - mj]
            itii -= mi
            itij -= mj
            bunretuiti = baio[itii, itij]
        if motoiti == -1:
            baio[motoi, motoj] = 2
            baio[motoi + mi, motoj + mj] = 3
        if motoiti == -2:
            baio[motoi, motoj] = 4
            baio[motoi + mi, motoj + mj] = 5
        if motoiti == -3:
            baio[motoi, motoj] = 6
            baio[motoi + mi, motoj + mj] = 7
        if motoiti < -3:
            baio[motoi + mi, motoj + mj] = motoiti * -1
            baio[motoi, motoj] = motoiti * -1

#分裂方向をランダムで決めて、そのままその方向に分裂させる。
def houkoukime():
    bunretuhoukou = random.randint(0,7)
    if bunretuhoukou == 0:
        bunretu(-1, -1)
    if bunretuhoukou == 1:
        bunretu(-1, 0)
    if bunretuhoukou == 2:
        bunretu(-1, 1)
    if bunretuhoukou == 3:
        bunretu(0, -1)
    if bunretuhoukou == 4:
        bunretu(0, 1)
    if bunretuhoukou == 5:
        bunretu(1, -1)
    if bunretuhoukou == 6:
        bunretu(1, 0)
    if bunretuhoukou == 7:
        bunretu(1, 1)

#実行部
w = plt.imshow(baio, cmap=plt.cm.get_cmap("tab20", 8))
plt.colorbar(extend="both")
plt.clim(0,7)
motoi = on
motoj = on
motoiti = baio[motoi, motoj]
houkoukime()

while t <= MAXT:
    bunretumainasu()
#ぐるぐる回る、真ん中だけ最初にやっとく
    motoi = on
    motoj = on
    motoiti = baio[motoi, motoj]
    houkoukime()
    for r in range(0, on):
        for k in range(0, 2 * r):
            if baio[on - r, on - r + k] < 0:
                motoi = on - r
                motoj = on - r + k
                motoiti = baio[motoi, motoj]
                houkoukime()
        for k in range(0, 2 * r):
            if baio[on - r + k, on + r] < 0:
                motoi = on - r + k
                motoj = on + r
                motoiti = baio[motoi, motoj]
                houkoukime()
        for k in range(0, 2 * r):
            if baio[on + r, on + r - k] < 0:
                motoi = on + r
                motoj = on + r - k
                motoiti = baio[motoi, motoj]
                houkoukime()
        for k in range(0, 2 * r):
            if baio[on + r - k, on - r] < 0:
                motoi = on + r - k
                motoj = on - r
                motoiti = baio[motoi, motoj]
                houkoukime()

    mainasureset()
    t += 1
    w = plt.imshow(baio, cmap=plt.cm.get_cmap("tab20", 8))
    w.set_data(baio)
    plt.pause(0.005)
for b in range(4, 8):
    kazu = np.where(baio == b)
    print(len(kazu[0]))
