from tumorsimu import Tumor_cell
from tumorsimu import Tumor_janitor
from cellsimu import Cell
from cellsimu import Janitor

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
