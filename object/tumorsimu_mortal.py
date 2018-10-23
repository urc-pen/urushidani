from tumorsimu import Tumor_cell
from tumorsimu import Tumor_janitor
from cellsimu import Cell
from cellsimu import Janitor
import argparse

#実行部
if __name__ == '__main__':
    Tumor_janitor.receive_value()
    Janitor.set_field()
    Janitor.set_heatmap()
    Tumor_cell.set_first_cell(Janitor.field, Janitor.on)
    Tumor_janitor.first_heatmap_graph()

    while Janitor.n < Janitor.MAXNUM:

        for cell in Cell.celllist:
            if cell.die == 0:
                cell.waittime_minus()
                cell.decide_prolife()
            else:
                pass

        Cell.radial_prolife(Janitor.field, Janitor.on)

        for cell in Cell.celllist:
            if cell.die == 0:
                cell.waittime_gamma(Janitor.AVERAGE,  Janitor.DISPERSION)
                if cell.driver_mutation == 0:
                    cell.count_all(Janitor.heatmap)
                    cell.decide_mortality(2000)
                    cell.mortal(Janitor.field)
            else:
                pass
            cell.update_heatmap(Janitor.heatmap)
        Tumor_janitor.append_cell_num()
        Tumor_janitor.plot_heatmap_graph()
        Janitor.count_cell_num()
        Janitor.t += 1

        if Janitor.n > Janitor.MAXNUM:
            break
    Tumor_janitor.count()
    Tumor_cell.list_adjust()
    print(Tumor_cell.driver_list)
