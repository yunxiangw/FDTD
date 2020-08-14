import numpy as np

class Geometry(object):

    def __init__(self, cell, eps_r, size):

        nx = cell.nx - 1
        ny = cell.ny - 1
        space_step = cell.space_step
        x_center, x_span, y_center, y_span = size
        x_min = int((x_center - x_span / 2) / space_step)
        x_max = int((x_center + x_span / 2) / space_step)
        y_min = int((y_center - y_span / 2) / space_step)
        y_max = int((y_center + y_span / 2) / space_step)

        self.eps = np.ones((nx, ny))
        self.eps[x_min:x_max, y_min:y_max] = eps_r