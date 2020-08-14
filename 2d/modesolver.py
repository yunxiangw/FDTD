import numpy as np


class ModeSolver(object):

        def __init__(self, res, width, freq, eps_wg, eps_bg):

            self.res = res
            self.width = width
            self.freq = freq
            self.eps_wg = eps_wg
            self.eps_bg = eps_bg

            self.A = self._cal_matrix()

        def _cal_matrix(self):

            total_w = int(3 * self.res * self.width)
            spacer_w = wg_w = int(self.res * self.width)

            second_order_fd = np.diag(-2 * np.ones(total_w)) + \
                              np.diag(np.ones(total_w-1), 1) + \
                              np.diag(np.ones(total_w-1), -1)
            second_order_fd *= self.res ** 2

            spacer_eps = self.eps_bg * np.ones(spacer_w)
            wg_eps = self.eps_wg * np.ones(wg_w)
            self.eps = np.diag(np.concatenate((spacer_eps, wg_eps, spacer_eps)))

            self.omega = 2 * np.pi * self.freq

            return second_order_fd + self.omega ** 2 * self.eps

        def solve(self):

            v, field_profiles = np.linalg.eig(self.A)

            mode_index = v > 0
            beta = np.sqrt(v[mode_index])
            ez = field_profiles[:, mode_index]

            sort_index = np.argsort(beta)[::-1]
            self.beta = beta[sort_index]
            ez = ez[:, sort_index]
            self.ez = ez / np.max(np.abs(ez), axis=0)
            self.hx = -beta / self.omega * ez
            self.hy = 1 / (1.0j * self.omega) * np.gradient(ez, 1/self.res, axis=0)
