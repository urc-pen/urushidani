import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from Cell import Cell
from Janitor import Janitor
from Tumorcell import Tumor_cell
from Tumorjanitor import Tumor_janitor

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-fu", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-si", type=int, default=155)
parser.add_argument("--AVERAGE", "-av", type=float, default=10)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-ma", type=int, default=3000)
parser.add_argument("--ENV", "-en", default=4000)
parser.add_argument("--MTRATE", "-mt", default=0.01, type=float)
parser.add_argument("--INTERVAL", "-in", default=5, type=int)
args = parser.parse_args()

if args.SIZE % 2 != 1:
    raise InvaridNumber("奇数を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("最大許容細胞数:{}".format(args.MAXNUM))
print("おおよその細胞周期:{}".format(args.AVERAGE))
print("細胞周期のばらつき:{}".format(args.DISPERSION))
print("環境収容力:{}".format(args.ENV))
print("ドライバー変異の起きる確率:{}".format(args.MTRATE))
print("描画のインターバル:{}".format(args.INTERVAL))

Tumor_janitor.receive_value(args.func, args.AVERAGE, args.DISPERSION, args.SIZE, args.MAXNUM, args.ENV, args.MTRATE, args.INTERVAL)
Janitor.set_field()
Janitor.set_heatmap()
Tumor_cell.set_first_cell(Janitor.field, Janitor.on)
Tumor_janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Tumor_cell.radial_prolife(Janitor.field, Janitor.on, Janitor.func, Janitor.MTRATE)

    Tumor_cell.countall(Janitor.heatmap)
    Janitor.refresh_heatmap()

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_gamma(Janitor.AVERAGE,  Janitor.DISPERSION)
            if cell.driver_mutation == 0:
                cell.dead_or_alive(Janitor.ENV, Janitor.field)
        cell.update_heatmap(Janitor.heatmap)

    Tumor_janitor.append_cell_num()
    Tumor_janitor.plot_heatmap_graph()
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

Tumor_janitor.count()
Tumor_cell.list_adjust()
print(Tumor_cell.driver_list)
