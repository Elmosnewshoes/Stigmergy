import numpy as np
from scipy.interpolate import Rbf

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm


# 2-d tests - setup scattered data
x = np.random.rand(100)*4.0-2.0
y = np.random.rand(100)*4.0-2.0
z = x*np.exp(-x**2-y**2)
ti = np.linspace(-2.0, 2.0, 100)
XI, YI = np.meshgrid(ti, ti)

# use RBF
rbf = Rbf(x, y, z, epsilon=0.5)
ZI = rbf(XI, YI)

# plot the result
# n = plt.normalize(-2., 2.)
fig, ax = plt.subplots()
# plt.subplot(1, 1, 1)
plt.pcolor(XI, YI, ZI, cmap=cm.jet)
# ax.plot(x, y, 100, z, cmap=cm.jet)
# plt.title('RBF interpolation - multiquadrics')
# plt.xlim(-2, 2)
# plt.ylim(-2, 2)
# plt.colorbar()
ax.scatter(x, y,100, z, cmap='viridis')
# ax.scatter(10*np.random.randn(100), 10*np.random.randn(100), 'o')
# ax.scatter
plt.show()


# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
#
# matplotlib.rcParams['axes.unicode_minus'] = False
# fig, ax = plt.subplots()
# ax.scatter(10*np.random.randn(100), 10*np.random.randn(100))
# ax.set_title('Using hyphen instead of Unicode minus')
# plt.show()
