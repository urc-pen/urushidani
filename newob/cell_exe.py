import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import argparse
from Cell import Cell
from Janitor import Janitor
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-f", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-s", type=int, default=155)
parser.add_argument("--AVERAGE", "-av", type=float, default=1)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-mn", type=int, default=3000)
parser.add_argument("--ENV", "-en", default=800)
args = parser.parse_args()

if args.SIZE % 2 != 1:
    raise InvaridNumber("奇数を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("最大許容細胞数:{}".format(args.MAXNUM))
print("おおよその細胞周期:{}".format(args.AVERAGE))
print("細胞周期のばらつき:{}".format(args.DISPERSION))
print("環境収容力:{}".format(args.ENV))

Janitor.receive_value(args.func, args.AVERAGE, args.DISPERSION, args.SIZE, args.MAXNUM, args.ENV)
Janitor.set_field()
Janitor.set_heatmap()
Cell.set_first_cell(Janitor.field, Janitor.on)
Janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Cell.radial_prolife(Janitor.field, Janitor.on, Janitor.func)

    Cell.countall(Janitor.heatmap)
    Janitor.refresh_heatmap()

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_gamma(Janitor.AVERAGE,  Janitor.DISPERSION)
            cell.dead_or_alive(Janitor.ENV, Janitor.field)
        cell.update_heatmap(Janitor.heatmap)

    Janitor.append_cell_num()
    Janitor.plot_heatmap_graph()
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

Janitor.count()
