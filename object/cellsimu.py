import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-f", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-s", type=int, default=155)
parser.add_argument("--AVERAGE", "-av", type=int, default=3)
parser.add_argument("--DISPERSION", "-di", type=int, default=2)
parser.add_argument("--MAXNUM", "-mn", type=int, default=7850)
args = parser.parse_args()

if args.SIZE % 2 != 1:
    raise InvaridNumber("奇数を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("最大許容細胞数:{}".format(args.MAXNUM))
print("おおよその細胞周期:{}".format(args.AVERAGE))
print("細胞周期のばらつき:{}".format(args.DISPERSION))

class Janitor:

    @classmethod
    def receive_value(cls):
        Janitor.AVERAGE = args.AVERAGE
        Janitor.DISPERSION = args.DISPERSION
        Janitor.SIZE = args.SIZE                    #フィールドの大きさ
        Janitor.on = int((Janitor.SIZE - 1) / 2)
        Janitor.t = 0
        Janitor.n = 0
        Janitor.MAXNUM = args.MAXNUM
        Janitor.threelist = []
        Janitor.fourlist = []
        Janitor.fivelist = []
        Janitor.sixlist = []
        Janitor.tlist = []

    @classmethod
    def set_field(cls):
        Janitor.field = np.full((Janitor.SIZE, Janitor.SIZE), -1, dtype=int)

    @classmethod
    def set_heatmap(cls):
        Janitor.heatmap = np.zeros((Janitor.SIZE, Janitor.SIZE))

    @classmethod
    def first_heatmap_graph(cls):
        fig = plt.figure(figsize=(10, 5))
        cmap = plt.cm.get_cmap("tab20", 7)
        defheatmap = Janitor.heatmap
        for n in range(0, 7):
            defheatmap[0, n] = n
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color="saddlebrown")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color="pink")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color="yellowgreen")
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color="skyblue")
        h = Janitor.ax2.imshow(defheatmap, cmap=cmap)
        fig.colorbar(h, cmap=cmap)
        for n in range(0, 7):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=cmap)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')


    @classmethod
    def plot_heatmap_graph(cls):
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color="saddlebrown")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color="pink")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color="yellowgreen")
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color="skyblue")
        Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap="tab20")
        plt.pause(0.1)

    @classmethod
    def count_cell_num(cls):
        Janitor.n = np.sum(Janitor.field > -1)

    @classmethod
    def append_cell_num(cls):
        Janitor.threelist.append(np.sum(Janitor.heatmap == 3))
        Janitor.fourlist.append(np.sum(Janitor.heatmap == 4))
        Janitor.fivelist.append(np.sum(Janitor.heatmap == 5))
        Janitor.sixlist.append(np.sum(Janitor.heatmap == 6))
        Janitor.tlist.append(Janitor.t)

    @classmethod
    def count(cls):
        for n in range(3, 7):
            print("cell{}:{}個".format(n, np.sum(Janitor.heatmap == n)))





class Cell:

    celllist = []
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.id = 0
        self.type = 0
        self.waittime = 0
        self.count = 0
        self.proliferation = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Cell(on, on)
        first_cell.id = 0
        first_cell.type = 0
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        Cell.celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def dire1(self, field):
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

    def dire2(self, field):
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
                    while proposi != -1:
                        obstacle = 1
                        obstacle += 1
                        ni += mi
                        nj += mj
                        proposi = field[ni, nj]
                    if proposi == -1:
                        obstacle_num.append(obstacle)
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

    def prolife(self, field):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Cell(ni, nj)
        cell_new.id = len(Cell.celllist)
        self.count += 1
        cell_new.count = self.count
        self.proliferation = 0
        if self.type <= 2:
            cell_new.type = int(self.type * 2 + 2)
            self.type = int(self.type * 2 + 1)
        elif self.type > 2:
            cell_new.type = self.type
        else:
            pass
        cell_new.move(field)
        Cell.celllist.append(cell_new)

    def move(self, field):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        if field[self.i, self.j] >= 0:
            id = field[self.i, self.j]
            Cell.celllist[id].i = ni
            Cell.celllist[id].j = nj
            Cell.celllist[id].move(field)
            field[self.i, self.j] = self.id
        else:
            field[self.i, self.j] = self.id

    @classmethod
    def radial_prolife(cls, field, on):
        if Cell.celllist[field[on, on]].proliferation == 1:
            getattr(Cell.celllist[field[on, on]], args.func)(field)
            Cell.celllist[field[on, on]].prolife(field)
        for r in range(0, on):
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r, on - r + k]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r, on - r + k]], args.func)(field)
                    Cell.celllist[field[on - r, on - r + k]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r + k, on + r]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r + k, on + r]], args.func)(field)
                    Cell.celllist[field[on - r + k, on + r]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r, on + r - k]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r, on + r - k]], args.func)(field)
                    Cell.celllist[field[on + r, on + r - k]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r - k, on - r]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r - k, on - r]], args.func)(field)
                    Cell.celllist[field[on + r - k, on - r]].prolife(field)


    def waittime_gamma(self, AVERAGE, DISPERSION):
        if self.waittime == 0:
            SHAPE = AVERAGE ** 2 / DISPERSION
            SCALE = DISPERSION / AVERAGE
            self.waittime = math.ceil(np.random.gamma(SHAPE, SCALE))

    def decide_prolife(self):
        if self.waittime == 0:
            self.proliferation = 1

    def waittime_minus(self):
        if self.waittime != 0:
            self.waittime -= 1

    def update_heatmap(self, heatmap):
        heatmap[self.i, self.j] = self.type





#実行部
if __name__ == '__main__':
    Janitor.receive_value()
    Janitor.set_field()
    Janitor.set_heatmap()
    Cell.set_first_cell(Janitor.field, Janitor.on)
    Janitor.first_heatmap_graph()

    while Janitor.n < Janitor.MAXNUM:

        for cell in Cell.celllist:
            cell.waittime_minus()
            cell.decide_prolife()

        Cell.radial_prolife(Janitor.field, Janitor.on)

        for cell in Cell.celllist:
            cell.waittime_gamma(Janitor.AVERAGE,  Janitor.DISPERSION)
            cell.update_heatmap(Janitor.heatmap)
        Janitor.append_cell_num()
        Janitor.plot_heatmap_graph()
        Janitor.count_cell_num()
        Janitor.t += 1

        if Janitor.n > Janitor.MAXNUM:
            break
    Janitor.count()
