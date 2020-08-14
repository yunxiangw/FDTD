import numpy as np


class Cell(object):

    def __init__(self, cell, space_step):
        self.space_step = space_step
        self.time_step = space_step / np.sqrt(2)
        self.nx, self.ny = self.__cal_num_of_grids(cell)
        self.e = np.zeros((self.nx, self.ny))
        self.h = np.zeros((self.nx, self.ny, 2))
        self.b = np.zeros((self.nx, self.ny, 2, 2))
        self.d = np.zeros((self.nx, self.ny, 2))
        self.constant_ezh = 1 / np.sqrt(2)
        self.constant_hxe = 1 / np.sqrt(2)
        self.constant_hye = 1 / np.sqrt(2)

    def __cal_num_of_grids(self, cell):
        x, y = cell
        nx = int(x / self.space_step + 1)
        ny = int(y / self.space_step + 1)
        return nx, ny

    def add_source(self, source):
        self.source_index = source.cal_index(self.space_step)

    def add_monitor(self, monitor):
        self.monitor_index = monitor.cal_index(self.space_step)
