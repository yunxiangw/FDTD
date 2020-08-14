import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

class Movie(object):

    def __init__(self, size):
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.ax.set_title('Ez')
        self.ax.set_xlabel('x (nm)')
        self.ax.set_ylabel('y (nm)')
        self.img = self.ax.imshow(np.zeros(size), extent=(0, 3000, 0, 3000), cmap='RdBu', vmin=-0.5, vmax=0.5, origin='lower')
        # self.fig.show()

        self.writer = FFMpegWriter(fps=60, bitrate=5000)

    def update(self, fields):
        self.img.set_data(fields)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.writer.grab_frame()

    def snapshot(self, **data):
        for name, fields in data.items():
            fig, ax = plt.subplots()
            ax.set_title(name)
            ax.set_xlabel('x (nm)')
            ax.set_ylabel('y (nm)')
            ax.imshow(fields, cmap='RdBu', extent=(-0.5, 3000.5, -0.5, 3000.5), vmin=-0.5, vmax=0.5, origin='lower')
            fig.savefig('{}.png'.format(name))
            fig.show()


