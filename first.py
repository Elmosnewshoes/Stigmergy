""" Test script """

import sys,time

import numpy as np
import matplotlib.pyplot as plt

# print(sys.executable)
# print(sys.version)

class domain:
    """  =================================
        The playground of the simulation
        =================================="""

    def __init__(self, h, w):
        """  =================================
            Initialize the class
            =================================="""

        self.unit = "mm" # scale
        self.resolution =  1.0 # pixels per unit

        self.height = h*self.resolution
        self.width = w*self.resolution



def randomwalk(dims = (256,256), n = 20, sigma=5, alpha=0.95, seed = 1):
    """ random walker """

    r, c = dims
    gen = np.random.RandomState(seed)
    pos = gen.rand(2,n)*((r,),(c,))
    old_delta = gen.randn(2,n)*sigma

    while True:
        delta = (1.-alpha)*gen.randn(2,n)*sigma + alpha *old_delta
        pos += delta
        for ii in range(n):
            if not (0. <= pos[0,ii]<r):
                pos[0,ii] = abs(pos[0,ii]%r)
            if not (0. <= pos[1,ii] < c):
                pos[1,ii] = abs(pos[1,ii] %c)
        old_delta = delta
        yield pos

def run(niter = 1000, doblit = True):

    fig, ax = plt.subplots(1,1)
    ax.set_aspect('equal')
    ax.set_xlim(0,255)
    ax.set_ylim(0,255)
    ax.hold(True)
    rw = randomwalk()
    x,y = next(rw)

    plt.show(False)
    plt.draw()

    if doblit:
        background = fig.canvas.copy_from_bbox(ax.bbox)

    points = ax.plot(x,y,'o')[0]
    tic = time.time()

    for ii in range(niter):
        x,y = next(rw)
        points.set_data(x,y)

        if doblit:
            fig.canvas.restore_region(background)
            ax.draw_artist(points)
            fig.canvas.blit(ax.bbox)
        else:
            fig.canvas.draw()
        plt.pause(0.01)


    print("Blit = {}s".format(time.time()-tic))




def plotting():
    x = range(12)
    plt.plot(x, np.power(x,2))
    plt.ylabel('some numbers')
    plt.show()

if __name__ == '__main__':
    run()
