import numpy as np
import os
import matplotlib.pyplot as plt

class Simulation(object):
    def __init__(self, cell, boundary, geometry, source, monitor, max_time, movie):

        self.cell = cell
        self.boundary = boundary
        self.source = source
        self.monitor = monitor

        # Add source
        cell.add_source(source)

        # Add monitor
        cell.add_monitor(monitor)

        # Add geometry
        self.eps = geometry.eps

        # Maximum time step
        self.max_time = int(max_time)

        self.movie = movie

    def update_fields(self, time):

        # Implement TFSF eigenmode source
        x, y = self.cell.source_index
        # y_min = y[0]
        # y_max = y[1]

        # Update the auxiliary field (Bx, By)
        self.__update_b(self.cell.b, self.cell.e)

        # Update magnetic field (Hx and Hy)
        self.__update_h(self.cell.h, self.cell.b)

        # factor_h = self.cell.time_step / self.cell.space_step
        # self.cell.h[y_min: y_max, x-1, 0] += factor_h * self.source.update_amplitude(time * self.cell.time_step)

        # Update the auxiliary field (Dz)
        self.__update_d(self.cell.d, self.cell.h)

        # Update electric field (Ez)
        self.__update_e(self.cell.e, self.cell.d)

        # actor_e = self.cell.time_step / (self.eps[y_min: y_max, x] * self.cell.space_step) * np.sqrt(self.eps[y_min: y_max, x])
        # self.cell.e[y_min: y_max, x] += factor_e * self.source.update_amplitude((time-1) * self.cell.time_step)

        self.cell.e[self.cell.source_index] += self.source.update_amplitude(time * self.cell.time_step)

    def __update_b(self, b_field, e_field):

        b_field[:, :, :, 1] = b_field[:, :, :, 0]

        b_field[:, :-1, 0, 0] = self.boundary.constant_bxb[:, :-1] * b_field[:, :-1, 0, 0] - \
                                self.boundary.constant_bxe[:, :-1] * (e_field[:, 1:] - e_field[:, :-1])

        b_field[:-1, :, 1, 0] = self.boundary.constant_byb[:-1, :] * b_field[:-1, :, 1, 0] + \
                                self.boundary.constant_bye[:-1, :] * (e_field[1:, :] - e_field[:-1, :])

    def __update_h(self, h_field, b_field):

        h_field[:, :-1, 0] = h_field[:, :-1, 0] + \
                             self.boundary.constant1_hxb[:, :-1] * b_field[:, :-1, 0, 0] - \
                             self.boundary.constant2_hxb[:, :-1] * b_field[:, :-1, 0, 1]

        h_field[:-1, :, 1] = self.cell.h[:-1, :, 1] + \
                             self.boundary.constant1_hyb[:-1, :] * b_field[:-1, :, 1, 0] - \
                             self.boundary.constant2_hyb[-1:, :] * b_field[:-1, :, 1, 1]

    def __update_d(self, d_field, h_field):

        d_field[1:-1, 1:-1, 1] = d_field[1:-1, 1:-1, 0]

        d_field[1:-1, 1:-1, 0] = self.boundary.constant_dd[1:-1, 1:-1] * d_field[1:-1, 1:-1, 0] + \
                                 self.boundary.constant_dh[1:-1, 1:-1] / self.eps[1:, 1:] * ((h_field[1:-1, 1:-1, 1] - h_field[:-2, 1:-1, 1]) -
                                                                                             (h_field[1:-1, 1:-1, 0] - h_field[1:-1, :-2, 0]))

    def __update_e(self, e_field, d_field):

        e_field[1:-1, 1:-1] = self.boundary.constant_ee[1:-1, 1:-1] * e_field[1:-1, 1:-1] + \
                              self.boundary.constant_ed[1:-1, 1:-1] * (d_field[1:-1, 1:-1, 0] - d_field[1:-1, 1:-1, 1])

    def run(self):
        with self.movie.writer.saving(self.movie.fig, 'animation.mp4', 100):
            for time in range(int(self.max_time)):
                self.update_fields(time)
                self.movie.update(self.cell.e[:, :]*5)
                self.monitor.record_data(self.cell.e[self.cell.monitor_index])
                # if time == 230:
                #     self.movie.snapshot(Ez=self.cell.e[:, :] * 15)
