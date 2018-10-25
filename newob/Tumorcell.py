from Cell import Cell
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Tumor_cell(Cell):
    driver_list = []
    def __init__(self, i, j):
        super().__init__(i, j)
        self.driver_mutation = 0
        self.mutation_id = 1
        self.driverflag = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Tumor_cell(on, on)
        first_cell.id = 0
        first_cell.type = 1
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        Cell.celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def prolife(self, field, MTRATE):
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
        cell_new.type = self.type

        if self.driver_mutation == 0 and self.type == 1:
            self.driverflag = np.random.choice([1, 0], p=[MTRATE, 1 - MTRATE])
            if self.driverflag == 1:
                self.type = 2
                self.driver_mutation = 1
                Tumor_cell.driver_list.append(self.mutation_id)
                self.driverflag = 0
        else:
            pass

        if cell_new.driver_mutation == 0 and cell_new.type == 1:
            cell_new.driverflag = np.random.choice([1, 0], p=[MTRATE, 1 - MTRATE])
            if cell_new.driverflag == 1:
                cell_new.type = 2
                cell_new.driver_mutation = 1
                Tumor_cell.driver_list.append(cell_new.mutation_id)
                cell_new.driverflag = 0
        else:
            pass

        cell_new.move(field)
        Cell.celllist.append(cell_new)

    @classmethod
    def radial_prolife(cls, field, on, func, MTRATE):
        if Cell.celllist[field[on, on]].proliferation == 1:
            getattr(Cell.celllist[field[on, on]], func)(field)
            Cell.celllist[field[on, on]].prolife(field, MTRATE)
        for r in range(0, on):
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r, on - r + k]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r, on - r + k]], func)(field)
                    Cell.celllist[field[on - r, on - r + k]].prolife(field, MTRATE)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r + k, on + r]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r + k, on + r]], func)(field)
                    Cell.celllist[field[on - r + k, on + r]].prolife(field, MTRATE)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r, on + r - k]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r, on + r - k]], func)(field)
                    Cell.celllist[field[on + r, on + r - k]].prolife(field, MTRATE)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r - k, on - r]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r - k, on - r]], func)(field)
                    Cell.celllist[field[on + r - k, on - r]].prolife(field, MTRATE)

    def tumor_waittime_gamma(self, AVERAGE, DISPERSION):
        if self.waittime == 0:
            SHAPE = ( AVERAGE / 1.5 ) ** 2 / DISPERSION
            SCALE = DISPERSION / ( AVERAGE / 1.5 )
            self.waittime = math.ceil(np.random.gamma(SHAPE / 2, SCALE / 2))

    @classmethod
    def list_adjust(cls):
        Tumor_cell.driver_list = list(set(Tumor_cell.driver_list))
        Tumor_cell.driver_list.sort()

    @classmethod
    def countall(cls, heatmap):
        Tumor_cell.one_num = np.sum(heatmap == 1)
        Tumor_cell.two_num = np.sum(heatmap == 2)
        Tumor_cell.three_num = np.sum(heatmap == 3)

    def dead_or_alive(self, ENV, field):
        if self.type == 1:
            self.mortal(Tumor_cell.one_num, ENV, field)
        if self.type == 2:
            self.mortal(Tumor_cell.two_num, ENV, field)
        if self.type == 3:
            self.mortal(Tumor_cell.three_num, ENV, field)

    @classmethod
    def list_adjust(cls):
        Tumor_cell.driver_list.sort()

    @classmethod
    def make_idlist(cls, field):
        Tumor_cell.idlist = []
        refid = np.random.choice(field[field > -1], 100, replace=False)
        for i in refid:
            Tumor_cell.idlist.append(Cell.celllist[i].mutation_id)
