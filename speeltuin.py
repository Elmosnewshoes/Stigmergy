import numpy as np
import small_functions as fun
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors
from map import MeshMap
import time
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!

from domain import AntDomain


def plot_surf(X,Y,Z):
    tic = time.time()
    fig = plt.figure()
    print("init fig in {:.4f} seconds".format(time.time()-tic))
    tic = time.time()
    ax = fig.gca()
    print("Set axis in {:.4f}".format(time.time()-tic))
    Z= np.add(Z,0.01)
    tic = time.time()
    the_plot = ax.pcolormesh(X,Y,Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()), cmap='PuBu')
    print("Make the contour in {:.4f}".format(time.time()-tic))
    ax.set_title('pcolor plot')
    tic = time.time()
    fig.colorbar(the_plot, ax = ax)
    print("Colorbar in {:.4f}".format(time.time()-tic))
    tic = time.time()
    plt.show()
    print("Render the plot in {:.4f}".format(time.time()-tic))
def run():
    D = AntDomain(size=[1000,1000], pitch = .5)
    D.set_gaussian(sigma = 5)
    print(D.Gaussian.map.sum())
    plot_surf(D.Gaussian.X,D.Gaussian.Y,D.Gaussian.map)

if __name__ =='__main__':
    run()
