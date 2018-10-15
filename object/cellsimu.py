import numpy as np
import random
import math
import fractions
import matplotlib.pyplot as plt
import seaborn

#argparse
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-f", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-s", type=int, default=55)
parser.add_argument("--MAXT", "-mt", type=int, default=60)
parser.add_argument("--SHAPE","-sh", type=int, default=2)
parser.add_argument("--SCALE","-sc", type=int, default=2)
args = parser.parse_args()

if args.SIZE % 2 !=1:
    raise InvaridNumber("奇数を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("分裂サイクルの継続時間:{}".format(args.MAXT))
print("形状母数:{}".format(args.SHAPE))
print("尺度母数:{}".format(args.SCALE))

SIZE = args.SIZE                    #フィールドの大きさ
on = int((SIZE - 1) / 2)            #原点の座標
t = 0
MAXT = args.MAXT             #分裂回数
SHAPE = args.SHAPE
SCALE = args.SCALE
field = np.full((SIZE, SIZE), -1, dtype=int)
heatmap = np.zeros((SIZE, SIZE))
celllist = []

class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    @classmethod
    def field_list_default(cls):
        first_cell = Cell(on, on)
        first_cell.id = 0
        first_cell.type = 0
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 1
        celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def dire1(self):
        direction = random.randint(0,7)
        if direction == 0:
            Cell.mi = -1
            Cell.mj = -1
        if direction == 1:
            Cell.mi = -1
            Cell.mj = 0
        if direction == 2:
            Cell.mi = -1
            Cell.mj = 1
        if direction == 3:
            Cell.mi = 0
            Cell.mj = -1
        if direction == 4:
            Cell.mi = 0
            Cell.mj = 1
        if direction == 5:
            Cell.mi = 1
            Cell.mj = -1
        if direction == 6:
            Cell.mi = 1
            Cell.mj = 0
        if direction == 7:
            Cell.mi = 1
            Cell.mj = 1

    def dire2(self):
        obstacle_num = []
        for mi in range(-1, 2):
            for mj in range(-1, 2):
                if mi == 0 and mj == 0:
                    continue
                ni = self.i + mi
                nj = self.j + mj
                id = field[self.i, self.j]
                proposi = field[ni, nj]
                if proposi == -1:
                    obstacle_num.append(1)
                else:
                    while proposi != -1 and ni != 0 and ni != SIZE - 1 and nj != 0 and nj != SIZE - 1:
                        obstacle = 1
                        obstacle += 1
                        ni += mi
                        nj += mj
                        proposi = field[ni, nj]
                    if proposi == -1:
                        obstacle_num.append(obstacle)
                    if ni == 0 or ni == SIZE - 1 or nj == 0 or nj == SIZE - 1:
                        obstacle_num.append(0)


        obstacle_ratio = []
        for i in range(0, 8):
            if obstacle_num[i] == 0:
                obstacle_ratio.append(0)
            else:
                obstacle_ratio.append(fractions.Fraction(1, obstacle_num[i]))
        obstacle_sum = sum(obstacle_ratio)
        dire_ratio = []
        for i in range(0, 8):
            if obstacle_ratio[i] == 0:
                dire_ratio.append(0)
            else:
                dire_ratio.append(fractions.Fraction(obstacle_ratio[i], obstacle_sum))

        if sum(dire_ratio) == 1:
            direction = np.random.choice([0,1,2,3,4,5,6,7], p=dire_ratio)
            if direction == 0:
                Cell.mi = -1
                Cell.mj = -1
            if direction == 1:
                Cell.mi = -1
                Cell.mj = 0
            if direction == 2:
                Cell.mi = -1
                Cell.mj = 1
            if direction == 3:
                Cell.mi = 0
                Cell.mj = -1
            if direction == 4:
                Cell.mi = 0
                Cell.mj = 1
            if direction == 5:
                Cell.mi = 1
                Cell.mj = -1
            if direction == 6:
                Cell.mi = 1
                Cell.mj = 0
            if direction == 7:
                Cell.mi = 1
                Cell.mj = 1

    def prolife(self):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Cell(ni, nj)
        cell_new.id = len(celllist)
        self.count += 1
        cell_new.count = self.count
        cell_new.waittime = 0
        self.proliferation = 0
        cell_new.proliferation = 0
        if self.type == 0:
            self.type = 1
            cell_new.type = 2
        elif self.type == 1:
            self.type = 3
            cell_new.type = 4
        elif self.type == 2:
            self.type = 5
            cell_new.type = 6
        else:
            cell_new.type = self.type
        cell_new.move()
        celllist.append(cell_new)

    def move(self):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        if field[self.i, self.j] >= 0:
            id = field[self.i, self.j]
            celllist[id].i = ni
            celllist[id].j = nj
            celllist[id].move()
            field[self.i, self.j] = self.id
        else:
            field[self.i, self.j] = self.id

    def waittime_gamma(self):
        if self.waittime == 0:
            self.waittime = math.ceil(np.random.gamma(SHAPE, SCALE))

    def decide_prolife(self):
        if self.waittime == 0:
            self.proliferation = 1

    def waittime_minus(self):
        if self.waittime != 0:
            self.waittime -= 1

    def update_heatmap(self):
        heatmap[self.i, self.j] = self.type

def first_heatmap():
    w = plt.imshow(heatmap, cmap=plt.cm.get_cmap("tab20", 8))
    plt.colorbar(extend="both")
    plt.clim(0,6)

def plot_heatmap():
    w = plt.imshow(heatmap,interpolation="nearest", cmap=plt.cm.get_cmap("tab20", 8))
    w.set_data(heatmap)
    plt.pause(0.005)

#実行部
Cell.field_list_default()
flag = False
first_heatmap()

while t <= MAXT:

    for cell in celllist:
        cell.waittime_minus()
        cell.decide_prolife()
        if cell.i == 0 or cell.i == SIZE - 1 or cell.j == 0 or cell.j == SIZE -1:
            flag = True
    if flag:
        break

    if celllist[field[on, on]].proliferation == 1:
        getattr(celllist[field[on, on]], args.func)()
        celllist[field[on, on]].prolife()
    for r in range(0, on):
        for k in range(0, 2 * r):
            if celllist[field[on - r, on - r + k]].proliferation == 1:
                getattr(celllist[field[on - r, on - r + k]], args.func)()
                celllist[field[on - r, on - r + k]].prolife()
        for k in range(0, 2 * r):
            if celllist[field[on - r + k, on + r]].proliferation == 1:
                getattr(celllist[field[on - r + k, on + r]], args.func)()
                celllist[field[on - r + k, on + r]].prolife()
        for k in range(0, 2 * r):
            if celllist[field[on + r, on + r - k]].proliferation == 1:
                getattr(celllist[field[on + r, on + r - k]], args.func)()
                celllist[field[on + r, on + r - k]].prolife()
        for k in range(0, 2 * r):
            if celllist[field[on + r - k, on - r]].proliferation == 1:
                getattr(celllist[field[on + r - k, on - r]], args.func)()
                celllist[field[on + r - k, on - r]].prolife()

    for cell in celllist:
        cell.waittime_gamma()
        cell.update_heatmap()
    plot_heatmap()

    t += 1
for b in range(3, 7):
    kazu = np.where(heatmap == b)
    print(len(kazu[0]))
