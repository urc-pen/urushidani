# coding: UTF-8
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import seaborn as sns
import sys
import fractions

#argparse
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-f", choices=["dire1", "dire2", "dire3"], default="dire2")
parser.add_argument("--SIZE", "-s", type=int, default=203)
parser.add_argument("--MAXT", "-mt", type=int, default=22)
parser.add_argument("--RATE", "-r", type=float, default=0.5)
args = parser.parse_args()

if args.SIZE % 2 !=1:
    raise InvaridNumber("奇数を入力してください")
if args.RATE < 0 or args.RATE > 1:
    raise InvaridNumber("0より大きく1以下の数値を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("分裂サイクルの継続時間:{}".format(args.MAXT))
print("分裂確率:{}".format(args.RATE))

SIZE = args.SIZE                    #フィールドの大きさ
bio = np.zeros((SIZE, SIZE))
on = int((SIZE - 1) / 2)            #原点の座標
bio[on, on] = -1
t = 0
MAXT = args.MAXT             #分裂回数
RATE = args.RATE

class Minus:
    def minus(self):               #ランダムで分裂する奴をマイナスにする関数
        for i in range(1, SIZE - 1):
            for j in range(1, SIZE - 1):
                if bio[i][j] != 0:
                    possibility = np.random.choice(["do", "dont"], p=[RATE, 1 - RATE])
                    if possibility == "do":
                        bio[i][j] = bio[i][j] * -1
                    else:
                        pass
        return bio

    def minusreset(self):               #マイナスをリセットする関数
        for i in range(0, SIZE):
            for j in range(0, SIZE):
                if bio[i][j] < 0:
                    bio[i][j] = bio[i][j] * -1
        return bio

    def minussearch(self):              #ぐるぐる回る、真ん中だけ最初にやっとく
        if bio[on, on] < 0:
            f = Prolife(on, on)
            getattr(f, args.func)()
        for r in range(0, on):
            for k in range(0, 2 * r):
                if bio[on - r, on - r + k] < 0:
                    f = Prolife(on - r, on - r + k)
                    getattr(f, args.func)()
            for k in range(0, 2 * r):
                if bio[on - r + k, on + r] < 0:
                    f = Prolife(on - r + k, on + r)
                    getattr(f, args.func)()
            for k in range(0, 2 * r):
                if bio[on + r, on + r - k] < 0:
                    f = Prolife(on + r, on + r - k)
                    getattr(f, args.func)()
            for k in range(0, 2 * r):
                if bio[on + r - k, on - r] < 0:
                    f = Prolife(on + r - k, on - r)
                    getattr(f, args.func)()

class Prolife:
    def __init__(self, i, j):
        self.prei = i
        self.prej = j

    def prolife(self, mi, mj):                 #分裂の関数。mi,mjを入れると分裂する
        proi = self.prei + mi
        proj = self.prej + mj
        proposi = bio[proi, proj]
        preposi = bio[self.prei, self.prej]

        if proposi == 0:
            if preposi == -1:
                bio[self.prei, self.prej] = 2
                bio[proi, proj] = 3
            if preposi == -2:
                bio[self.prei, self.prej] = 4
                bio[proi, proj] = 5
            if preposi == -3:
                bio[self.prei, self.prej] = 6
                bio[proi, proj] = 7
            if preposi < -3:
                bio[self.prei, self.prej] = preposi * -1
                bio[proi, proj] = preposi * -1
            return bio

        if proposi != 0:
            while proposi != 0 and proi != 0 and proi != SIZE - 1 and proj != 0 and proj != SIZE - 1:
                proi += mi
                proj += mj
                proposi = bio[proi, proj]
                if proposi == 0 or proi == 0 or proi == SIZE - 1 or proj == 0 or proj == SIZE - 1:
                    pass
            while proi != self.prei + mi or proj != self.prej + mj:
                bio[proi, proj] = bio[proi - mi, proj - mj]
                proi -= mi
                proj -= mj
                proposi = bio[proi, proj]
            if preposi == -1:
                bio[self.prei, self.prej] = 2
                bio[self.prei + mi, self.prej + mj] = 3
            if preposi == -2:
                bio[self.prei, self.prej] = 4
                bio[self.prei + mi, self.prej + mj] = 5
            if preposi == -3:
                bio[self.prei, self.prej] = 6
                bio[self.prei + mi, self.prej + mj] = 7
            if preposi < -3:
                bio[self.prei + mi, self.prej + mj] = preposi * -1
                bio[self.prei, self.prej] = preposi * -1
            return bio

    def dire1(self):          #分裂方向をランダムで決めて、そのままその方向に分裂させる。
        direction = random.randint(0,7)
        if direction == 0:
            self.prolife(-1, -1)
        if direction == 1:
            self.prolife(-1, 0)
        if direction == 2:
            self.prolife(-1, 1)
        if direction == 3:
            self.prolife(0, -1)
        if direction == 4:
            self.prolife(0, 1)
        if direction == 5:
            self.prolife(1, -1)
        if direction == 6:
            self.prolife(1, 0)
        if direction == 7:
            self.prolife(1, 1)

    def dire2(self):      #分裂場所の空き具合によって方向の確率が決まって分裂する。
        jamakazu = []
        for mmi in range(-1, 2):
            for mmj in range(-1, 2):
                if mmi != 0 or mmj != 0:
                    proi = self.prei + mmi
                    proj = self.prej + mmj
                    proposi = bio[proi, proj]
                    if proposi == 0:
                        jamakazu.append(1)
                    else:
                        while proposi != 0 and proi != 0 and proi != SIZE - 1 and proj != 0 and proj != SIZE - 1:
                            jama = 1
                            jama += 1
                            proi += mmi
                            proj += mmj
                            proposi = bio[proi, proj]
                        if proposi == 0:
                            jamakazu.append(jama)
                        if proi == 0 or proi == SIZE - 1 or proj == 0 or proj == SIZE - 1:
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
            direction = np.random.choice([0,1,2,3,4,5,6,7], p=houkouwari)
            if direction == 0:
                self.prolife(-1, -1)
            if direction == 1:
                self.prolife(-1, 0)
            if direction == 2:
                self.prolife(-1, 1)
            if direction == 3:
                self.prolife(0, -1)
            if direction == 4:
                self.prolife(0, 1)
            if direction == 5:
                self.prolife(1, -1)
            if direction == 6:
                self.prolife(1, 0)
            if direction == 7:
                self.prolife(1, 1)
        else:
            bio[self.prei, self.prej] = bio[self.prei, self.prej] * -1
            return bio

    def dire3(self):    #空いている場所にしか分裂しない。
        houkouwari = []
        jamakazu = []
        for mmi in range(-1, 2):
            for mmj in range(-1, 2):
                if mmi != 0 or mmj != 0:
                    proi = self.prei + mmi
                    proj = self.prej + mmj
                    proposi = bio[proi, proj]
                    if proposi == 0:
                        jamakazu.append(1)
                    else:
                        jamakazu.append(0)
        for i in range(0, 8):
            if sum(jamakazu) != 0:
                houkouwari.append(fractions.Fraction(jamakazu[i], sum(jamakazu)))
            else:
                houkouwari = [0, 0, 0, 0, 0, 0, 0, 0]
        if sum(houkouwari) == 1:
            direction = np.random.choice([0,1,2,3,4,5,6,7], p=houkouwari)
            if direction == 0:
                self.prolife(-1, -1)
            if direction == 1:
                self.prolife(-1, 0)
            if direction == 2:
                self.prolife(-1, 1)
            if direction == 3:
                self.prolife(0, -1)
            if direction == 4:
                self.prolife(0, 1)
            if direction == 5:
                self.prolife(1, -1)
            if direction == 6:
                self.prolife(1, 0)
            if direction == 7:
                self.prolife(1, 1)
        else:
            bio[self.prei, self.prej] = bio[self.prei, self.prej] * -1
            return bio

class Heatmap:
    def firstheat(self):
        w = plt.imshow(bio, cmap=plt.cm.get_cmap("tab20", 8))
        plt.colorbar(extend="both")
        plt.clim(0,7)

    def contheat(self):
        w = plt.imshow(bio,interpolation="nearest", cmap=plt.cm.get_cmap("tab20", 8))
        w.set_data(bio)
        plt.pause(0.005)

#実行部
h = Heatmap()
m = Minus()
h.firstheat()
p = Prolife(on, on)
getattr(p, args.func)()
while t <= MAXT:
    m.minus()
    m.minussearch()
    m.minusreset()
    h.contheat()
    t += 1

for b in range(4, 8):
    kazu = np.where(bio == b)
    print(len(kazu[0]))
