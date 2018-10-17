from cellsimu import Cell
from cellsimu import Janitor
import numpy as np
import random
import math
import fractions
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mutationrate", "-mr", default=0.01, type=float)
args = parser.parse_args()

class Tumor_cell(Cell):
    def __init__(self, i, j):
        super().__init__(i, j)
        self.driver_mutation = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Tumor_cell(on, on)
        first_cell.id = 0
        first_cell.type = 0
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        Cell.celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def prolife(self, field):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Tumor_cell(ni, nj)
        cell_new.id = len(Cell.celllist)
        self.count += 1
        cell_new.count = self.count
        self.proliferation = 0
        self.driver_mutation = np.random.choice([1, 0], p=[args.mutationrate, 1 - args.mutationrate])
        cell_new.driver_mutation = np.random.choice([1, 0], p=[args.mutationrate, 1 - args.mutationrate])
        if self.type <= 2:
            cell_new.type = int(self.type * 2 + 2)
            self.type = int(self.type * 2 + 1)
        elif self.type > 2:
            cell_new.type = self.type
        else:
            pass
        if self.driver_mutation == 1:
            self.type = 7
        if cell_new.driver_mutation == 1:
            cell_new.type = 7
        cell_new.move(field)
        Cell.celllist.append(cell_new)

    def tumor_waittime_gamma(self, AVERAGE, DISPERSION):
        if self.waittime == 0:
            SHAPE = ( AVERAGE / 2 ) ** 2 / DISPERSION
            SCALE = DISPERSION / ( AVERAGE / 2 )
            self.waittime = math.ceil(np.random.gamma(SHAPE / 2, SCALE / 2))



class Tumor_janitor(Janitor):
    @classmethod
    def receive_value(cls):
        super().receive_value()
        Janitor.sevenlist = []

    @classmethod
    def append_cell_num(cls):
        super().append_cell_num()
        Janitor.sevenlist.append(np.sum(Janitor.heatmap == 7))


    @classmethod
    def first_heatmap_graph(cls):
        fig = plt.figure(figsize=(10, 5))
        cmap = plt.cm.get_cmap("tab20", 8)
        defheatmap = Janitor.heatmap
        for n in range(0, 8):
            defheatmap[0, n] = n
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color="MediumPurple")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color="RosyBrown")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color="Gray")
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color="Khaki")
        Janitor.ax1.plot(Janitor.tlist, Janitor.sevenlist, label="7", color="skyblue")
        h = Janitor.ax2.imshow(defheatmap, cmap=cmap)
        fig.colorbar(h, cmap=cmap)
        for n in range(0, 8):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=cmap)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')

    @classmethod
    def plot_heatmap_graph(cls):
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color="MediumPurple")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color="RosyBrown")
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color="Gray")
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color="Khaki")
        Janitor.ax1.plot(Janitor.tlist, Janitor.sevenlist, label="7", color="skyblue")
        Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap="tab20")
        plt.pause(0.1)

    @classmethod
    def count(cls):
        super().count()
        print("cell{}:{}個".format(7, np.sum(Janitor.heatmap == 7)))


#実行部
if __name__ == '__main__':
    Tumor_janitor.receive_value()
    Janitor.set_field()
    Janitor.set_heatmap()
    Tumor_cell.set_first_cell(Janitor.field, Janitor.on)
    Tumor_janitor.first_heatmap_graph()

    while Janitor.n < Janitor.MAXNUM:

        for cell in Cell.celllist:
            cell.waittime_minus()
            cell.decide_prolife()

        Cell.radial_prolife(Janitor.field, Janitor.on)

        for cell in Cell.celllist:
            if cell.driver_mutation == 1:
                cell.tumor_waittime_gamma(Janitor.AVERAGE, Janitor.DISPERSION)
            else:
                cell.waittime_gamma(Janitor.AVERAGE,  Janitor.DISPERSION)
            cell.update_heatmap(Janitor.heatmap)
        Tumor_janitor.append_cell_num()
        Tumor_janitor.plot_heatmap_graph()
        Janitor.count_cell_num()
        Janitor.t += 1

        if Janitor.n > Janitor.MAXNUM:
            break
    Tumor_janitor.count()
