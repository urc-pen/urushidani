import math
import numpy as np
import random
import pandas as pd

class Plotter:
    @classmethod
    def receive_value(cls, POISSON):
        Plotter.POISSON = POISSON

    @classmethod
    def plot_mutation(cls, idlist, mutlist, POISSON):
        finaldic = {}
        for i in range(0, len(idlist)):
            firstdic = {}
            seconddic = {}
            thirddic = {}
            varno = idlist[i]
            columnno = idlist[i]
            while varno != 1:
                if varno in mutlist:
                    firstdic = {str(varno):np.random.poisson(POISSON) + 1}
                    seconddic.update(firstdic)
                else:
                    firstdic = {str(varno):np.random.poisson(POISSON)}
                    seconddic.update(firstdic)

                varno = math.floor(varno / 2)

                if varno == 1:
                    thirddic = {"cell" + str(columnno):seconddic}
                    break

            finaldic.update(thirddic.copy())
        print(finaldic)

        for m in range(0, len(idlist)):
            key = "cell" + str(idlist[m])
            innerkey = tuple(finaldic[key].keys())
            for i in innerkey:
                element = finaldic[key][i]
                if element == 1 or element == 0:
                    if int(i) in mutlist:
                        del finaldic[key][i]
                        finaldic[key]["D" + i] = element
                    else:
                        del finaldic[key][i]
                        finaldic[key]["N" + i] = element

                if element >= 2:
                    if int(i) in mutlist:
                        del finaldic[key][i]
                        finaldic[key]["D" + i] = 1
                    else:
                        del finaldic[key][i]
                        finaldic[key]["N" + i] = 1

                    for j in range(2, element + 1):
                        finaldic[key]["N" + i + "_" + str(j)] = 1
                else:
                    pass

        print(finaldic)

        df1 = pd.DataFrame(finaldic)
        df2 = df1.fillna(0)
        Plotter.df = df2.astype(int)
