from cell import Cell
from source import SineGaussianSource, ModeSource
from monitor import Monitor
from simulation import Simulation
from movie import Movie
from pml import PML
from geometry import Geometry

# Define simulation region
cell = Cell(cell=(3.0, 3.0), space_step=0.01)

# Define Boundary Condition
pml = PML(cell, thickness=10, reflection=1e-7)

# Define geometry
geo = Geometry(cell, eps_r=12, size=(1.5, 0.18, 1.5, 3.0))

# Define the source
source = SineGaussianSource(center=(1.5, 0.5), wavelength=0.95, width=0.1)
# source = ModeSource(center=(0.5, 1.5), wg_w=0.18, res=1/0.01, wavelength=0.95, width=0.1)

# Define the monitor
monitor = Monitor(center=(1.5, 2.5))

# Define movie plotter
plotter = Movie((301, 301))

# Initiate FDTD simulation
sim = Simulation(cell=cell, boundary=pml, geometry=geo, source=source, monitor=monitor, max_time=5e3, movie=plotter)

# Running FDTD simulation
sim.run()

# Plot the Ez(t) at the probe location
monitor.plot()

# Do FFT and plot Ez(w)
# monitor.frequency_spectrum(cell.time_step)




