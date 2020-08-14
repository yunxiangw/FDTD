import numpy as np
import matplotlib.pyplot as plt


class Monitor(object):

    def __init__(self, center):
        self.center = center
        self.data = []

    def cal_index(self, space_step):
        x, y = self.center
        x = int(x / space_step + 1)
        y = int(y / space_step + 1)
        return x, y

    def record_data(self, data):
        self.data.append(data)

    def plot(self):
        if self.data is not None:
            plt.figure()
            plt.xlabel('Time Step')
            plt.ylabel('log($E_z$)')
            plt.ylim((1e-14, 1))
            plt.semilogy(np.abs(self.data), linewidth=0.5)
            plt.savefig('Ez at probe location.png')
            np.savetxt('ez.txt', self.data, delimiter='    ')
            plt.show()
        else:
            raise UserWarning('No data is recorded')

    def frequency_spectrum(self, dt):
        # Number of sampling points
        num = len(self.data)
        # FFT
        yf = np.fft.fft(self.data)
        yf = 2.0/num * np.abs(yf[:num//2])
        xf = np.linspace(0, 1/(2 * dt), num/2)
        # Slice from 400nm to 1200nm
        yw = yf[(xf >= 1/1.2) & (xf <= 1/0.4)]
        xw = 1 / xf[(xf >= 1/1.2) & (xf <= 1/0.4)] * 1000
        # Plot frequency spectrum
        fig, ax = plt.subplots()
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Magnitude')
        ax.plot(xw, yw)
        plt.savefig('FFT of Ez at probe location.png')
        plt.show()