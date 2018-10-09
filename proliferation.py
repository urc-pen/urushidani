# coding: UTF-8
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import seaborn as sns
import sys
import fractions

#argparseの部分
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("func", choices=["dire1", "dire2", "dire3"])
parser.add_argument("size", type=int)
parser.add_argument("MAXT", type=int)
parser.add_argument("rate", type=float)
args = parser.parse_args()

if args.size % 2 !=1:
    raise InvaridNumber("奇数を入力してください")
if args.rate < 0 or args.rate > 1:
    raise InvaridNumber("0より大きく1以下の数値を入力してください")

#size*sizeのbaioというフィールドを作って、原点の座標(on,on)＝1と定めた。
size = args.size                   #フィールドの大きさ
baio = np.zeros((size, size))
on = int((size - 1) / 2)
baio[on, on] = -1
t = 0
MAXT = args.MAXT             #分裂回数

#ランダムで分裂する奴をマイナスにする関数
def bunretumainasu():
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if baio[i][j] != 0:
                bunretu = np.random.choice(["do", "dont"], p=[args.rate, 1 - args.rate])
                if bunretu == "do":
                    baio[i][j] = baio[i][j] * -1
                else:
                    pass
#マイナスをリセットする関数
def mainasureset():
    for i in range(0, size):
        for j in range(0, size):
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
        while bunretuiti != 0 and itii != 0 and itii != size - 1 and itij != 0 and itij != size - 1:
            itii += mi
            itij += mj
            bunretuiti = baio[itii, itij]
            if bunretuiti == 0 or itii == 0 or itii == size - 1 or itij == 0 or itij == size - 1:
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
def dire1():
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

#分裂場所の空き具合によって方向の確率が決まって分裂する。
def dire2():
    jamakazu = []
    for mmi in range(-1, 2):
        for mmj in range(-1, 2):
            if mmi != 0 or mmj != 0:
                itii = motoi + mmi
                itij = motoj + mmj
                bunretuiti = baio[itii, itij]
                if bunretuiti == 0:
                    jamakazu.append(1)
                else:
                    while bunretuiti != 0 and itii != 0 and itii != size - 1 and itij != 0 and itij != size - 1:
                        jama = 1
                        jama += 1
                        itii += mmi
                        itij += mmj
                        bunretuiti = baio[itii, itij]
                    if bunretuiti == 0:
                        jamakazu.append(jama)
                    if itii == 0 or itii == size - 1 or itij == 0 or itij == size - 1:
                        jamakazu.append(0)
            else:
                pass

    jamawari = []
    for i in range(0, 8):
        if jamakazu[i] == 0:
            jamawari.append(0)
        else:
            jamawari.append(fractions.Fraction(1, jamakazu[i]))
    jamasum = sum(jamawari)
    houkouwari = []
    for i in range(0, 8):
        if jamawari[i] == 0:
            houkouwari.append(0)
        else:
            houkouwari.append(fractions.Fraction(jamawari[i], jamasum))

    if sum(houkouwari) == 1:
        bunretuhoukou = np.random.choice([0,1,2,3,4,5,6,7], p=houkouwari)
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
    else:
        baio[motoi, motoj] = baio[motoi, motoj] * -1

#空いている場所にしか分裂しない。
def dire3():
    houkouwari = []
    jamakazu = []
    for mmi in range(-1, 2):
        for mmj in range(-1, 2):
            if mmi != 0 or mmj != 0:
                itii = motoi + mmi
                itij = motoj + mmj
                bunretuiti = baio[itii, itij]
                if bunretuiti == 0:
                    jamakazu.append(1)
                else:
                    jamakazu.append(0)
    for i in range(0, 8):
        if sum(jamakazu) != 0:
            houkouwari.append(fractions.Fraction(jamakazu[i], sum(jamakazu)))
        else:
            houkouwari = [0, 0, 0, 0, 0, 0, 0, 0]
    if sum(houkouwari) == 1:
        bunretuhoukou = np.random.choice([0,1,2,3,4,5,6,7], p=houkouwari)
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
    else:
        baio[motoi, motoj] = baio[motoi, motoj] * -1


#実行部
w = plt.imshow(baio, cmap=plt.cm.get_cmap("tab20", 8))
plt.colorbar(extend="both")
plt.clim(0,7)
motoi = on
motoj = on
motoiti = baio[motoi, motoj]
eval(args.func)()

while t <= MAXT:
    bunretumainasu()
#ぐるぐる回る、真ん中だけ最初にやっとく
    motoi = on
    motoj = on
    motoiti = baio[motoi, motoj]
    eval(args.func)()
    for r in range(0, on):
        for k in range(0, 2 * r):
            if baio[on - r, on - r + k] < 0:
                motoi = on - r
                motoj = on - r + k
                motoiti = baio[motoi, motoj]
                eval(args.func)()
        for k in range(0, 2 * r):
            if baio[on - r + k, on + r] < 0:
                motoi = on - r + k
                motoj = on + r
                motoiti = baio[motoi, motoj]
                eval(args.func)()
        for k in range(0, 2 * r):
            if baio[on + r, on + r - k] < 0:
                motoi = on + r
                motoj = on + r - k
                motoiti = baio[motoi, motoj]
                eval(args.func)()
        for k in range(0, 2 * r):
            if baio[on + r - k, on - r] < 0:
                motoi = on + r - k
                motoj = on - r
                motoiti = baio[motoi, motoj]
                eval(args.func)()

    mainasureset()
    t += 1
    w = plt.imshow(baio, cmap=plt.cm.get_cmap("tab20", 8))
    w.set_data(baio)
    plt.pause(0.005)
for b in range(4, 8):
    kazu = np.where(baio == b)
    print(len(kazu[0]))
