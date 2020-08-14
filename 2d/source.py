import numpy as np
from modesolver import ModeSolver


class SineGaussianSource(object):

    def __init__(self, center, wavelength, width):
        self.center = center
        self.omega = 2 * np.pi / wavelength
        self.sigma = 2 / self.omega * (wavelength / width)

    def cal_index(self, space_step):
        x, y = self.center
        x = int(x / space_step)
        y = int(y / space_step)
        return x, y

    def update_amplitude(self, time):
        amplitude = np.sin(self.omega * (time - 4 * self.sigma)) * np.exp(-((time - 4 * self.sigma) / self.sigma) ** 2)
        return amplitude


class ModeSource(object):

    def __init__(self, center, wg_w, res, wavelength, width):
        self.center = center
        self.wg_w = wg_w
        self.omega = 2 * np.pi / wavelength
        self.sigma = 2 / self.omega * (wavelength / width)
        # solve the eigenmodes
        self.modesolver = ModeSolver(res=res, width=wg_w, freq=1/wavelength, eps_bg=1, eps_wg=12)
        self.modesolver.solve()
        self.j = self.modesolver.ez[:, 0]

    def cal_index(self, space_step):
        x, y = self.center
        x = int(x / space_step)
        y_min = int((y - 1.5 * self.wg_w) / space_step)
        y_max = int((y + 1.5 * self.wg_w) / space_step)
        y = [y_min, y_max]

        return x, y

    def update_amplitude(self, time):
        amplitude = self.j * np.sin(self.omega * (time - 4 * self.sigma)) * np.exp(-((time - 4 * self.sigma) / self.sigma) ** 2)
        return amplitude
