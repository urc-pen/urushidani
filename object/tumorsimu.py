from cellsimu import Cell
from cellsimu import Janitor
import numpy as np
import random
import math
import fractions
import matplotlib.pyplot as plt
import argparse
from matplotlib.colors import LinearSegmentedColormap
parser = argparse.ArgumentParser()
parser.add_argument("--mutationrate", "-mr", default=0.0001, type=float)
args = parser.parse_args()

print("ドライバー変異の起きる確率:{}".format(args.mutationrate))

class Tumor_cell(Cell):
    driver_list = []
    def __init__(self, i, j):
        super().__init__(i, j)
        self.driver_mutation = 0
        Janitor.mutationrate = args.mutationrate
        self.mutation_id = 1

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

    def prolife(self, field, mutationrate):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Tumor_cell(ni, nj)
        cell_new.id = len(Cell.celllist)
        self.count += 1
        self.mutation_id = self.mutation_id * 2
        cell_new.mutation_id = self.mutation_id * 2 + 1
        cell_new.count = self.count
        self.proliferation = 0
        cell_new.driver_mutation = self.driver_mutation

        if self.driver_mutation == 0:
            self.driver_mutation = np.random.choice([1, 0], p=[mutationrate, 1 - mutationrate])
        if self.driver_mutation == 1:
            self.type = 2
            Tumor_cell.driver_list.append(self.mutation_id)

        if cell_new.driver_mutation == 0:
            cell_new.driver_mutation = np.random.choice([1, 0], p=[mutationrate, 1 - mutationrate])
        if cell_new.driver_mutation == 1:
            cell_new.type = 2
            Tumor_cell.driver_list.append(cell_new.mutation_id)

        if self.type == 0:
            cell_new.type = 1
            self.type = 1
        elif self.type >= 1:
            cell_new.type = self.type
            self.type = self.type
        else:
            pass

        cell_new.move(field)
        Cell.celllist.append(cell_new)

    @classmethod
    def radial_prolife(cls, field, on, func, mutationrate):
        if Cell.celllist[field[on, on]].proliferation == 1:
            getattr(Cell.celllist[field[on, on]], func)(field)
            Cell.celllist[field[on, on]].prolife(field, mutationrate)
        for r in range(0, on):
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r, on - r + k]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r, on - r + k]], func)(field)
                    Cell.celllist[field[on - r, on - r + k]].prolife(field, mutationrate)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r + k, on + r]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r + k, on + r]], func)(field)
                    Cell.celllist[field[on - r + k, on + r]].prolife(field, mutationrate)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r, on + r - k]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r, on + r - k]], func)(field)
                    Cell.celllist[field[on + r, on + r - k]].prolife(field, mutationrate)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r - k, on - r]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r - k, on - r]], func)(field)
                    Cell.celllist[field[on + r - k, on - r]].prolife(field, mutationrate)

    def tumor_waittime_gamma(self, AVERAGE, DISPERSION):
        if self.waittime == 0:
            SHAPE = ( AVERAGE / 1.5 ) ** 2 / DISPERSION
            SCALE = DISPERSION / ( AVERAGE / 1.5 )
            self.waittime = math.ceil(np.random.gamma(SHAPE / 2, SCALE / 2))

    @classmethod
    def list_adjust(cls):
        Tumor_cell.driver_list = list(set(Tumor_cell.driver_list))
        Tumor_cell.driver_list.sort()



class Tumor_janitor(Janitor):
    @classmethod
    def receive_value(cls):
        super().receive_value()
        Janitor.t = 3
        Janitor.onelist = [0]
        Janitor.twolist = [0]
        Janitor.mutationrate = args.mutationrate

    @classmethod
    def append_cell_num(cls):
        Janitor.onelist.append(np.sum(Janitor.heatmap == 1))
        Janitor.twolist.append(np.sum(Janitor.heatmap == 2))
        Janitor.tlist.append(Janitor.t)

    @classmethod
    def first_heatmap_graph(cls):
        fig = plt.figure(figsize=(10, 5))
        Janitor.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=3)
        defheatmap = Janitor.heatmap
        for n in range(0, 3):
            defheatmap[0, n] = n
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutation", color=Janitor.colors[1])
        Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: driver mutation", color=Janitor.colors[2])
        h = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        fig.colorbar(h, cmap=Janitor.cm)
        for n in range(0, 3):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')

    @classmethod
    def plot_heatmap_graph(cls):
        Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutation", color=Janitor.colors[1])
        Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: driver mutation", color=Janitor.colors[2])
        Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
        plt.pause(0.01)

    @classmethod
    def count(cls):
        for n in range(1, 3):
            print("cell{}:{}個".format(n, np.sum(Janitor.heatmap == n)))
