import numpy as np


class PML(object):

    def __init__(self, cell, thickness=10, reflection=1e-6):

        nx = cell.nx
        ny = cell.ny

        delta_t = cell.time_step
        delta_x = cell.space_step

        sigma_max = - 1 / (thickness * delta_x) * np.log(reflection)

        sigma_x = np.zeros((2 * nx, ny))
        sigma_y = np.zeros((nx, 2 * ny))

        loss_x = sigma_max * (np.mgrid[1: 2 * thickness + 1, 0:ny][0] / (2 * thickness)) ** 3
        loss_y = sigma_max * (np.mgrid[0:nx, 1: 2 * thickness + 1][1] / (2 * thickness)) ** 3

        sigma_x[: 2 * thickness, :] = loss_x[::-1, :]
        sigma_x[2 * (nx - thickness) - 1: -1, :] = loss_x
        sigma_y[:, :2 * thickness] = loss_y[:, ::-1]
        sigma_y[:, 2 * (ny - thickness) - 1: -1] = loss_y

        self.constant_bxb = (1 - 0.5 * delta_t * sigma_y[:, 1::2]) / (1 + 0.5 * delta_t * sigma_y[:, 1::2])
        self.constant_bxe = delta_t / ((1 + 0.5 * delta_t * sigma_y[:, 1::2]) * delta_x)
        self.constant_byb = (1 - 0.5 * delta_t * sigma_x[1::2, :]) / (1 + 0.5 * delta_t * sigma_x[1::2, :])
        self.constant_bye = delta_t / ((1 + 0.5 * delta_t * sigma_x[1::2, :]) * delta_x)

        self.constant_dd = (1 - 0.5 * delta_t * sigma_x[::2, :]) / (1 + 0.5 * delta_t * sigma_x[::2, :])
        self.constant_dh = delta_t / ((1 + 0.5 * delta_t * sigma_x[::2, :]) * delta_x)

        self.constant1_hxb = 1 + 0.5 * delta_t * sigma_x[::2, :]
        self.constant2_hxb = 1 - 0.5 * delta_t * sigma_x[::2, :]

        self.constant1_hyb = 1 + 0.5 * delta_t * sigma_y[:, ::2]
        self.constant2_hyb = 1 - 0.5 * delta_t * sigma_y[:, ::2]

        self.constant_ee = (1 - 0.5 * delta_t * sigma_y[:, ::2]) / (1 + 0.5 * delta_t * sigma_y[:, ::2])
        self.constant_ed = 1 / (1 + 0.5 * delta_t * sigma_y[:, ::2])



