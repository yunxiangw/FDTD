import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 1, 51)
y = []
for a in x:
    if a < 0:
        y.append(-a)
    else:
        y.append(a)

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()