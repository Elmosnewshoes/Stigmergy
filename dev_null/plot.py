""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """


import numpy as np
from matplotlib import cm, gridspec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import time
from domain import AntDomain

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

from ant import Ant

plt.ion()

# for ease of use, save some colorschemes
cmaps = {'blue': 'PuBu',
         'grey_reverse': 'grey_r',
         }

class MapPlot():
    """ ===================
        do the plotting of the pheromone map
        and the scatter of ant locations
        ==================="""

    def __init__(self,X,Y, colormap = 'blue', n = 10):
        """ ================
            initialize the class
            ================"""
        # timing variables
        self.draw_time = 0
        self.surf_time = 0

        # local copy of meshgrid
        self.X = X
        self.Y = Y

        # vectors for entropy (hor and vertical)
        self.E = np.zeros((n,1))
        self.T = np.arange(n)
        self.E[self.E==0] = np.nan
        self.t = 0 #keep track of position

        # define the colormap to use
        self.cmap = plt.get_cmap(cmaps['blue'] )

        # define the plot variables
        plt.ion()
        self.fig = plt.figure(figsize=(8,6))
        self.ax = self.fig.gca()

        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        self.ax_imscat = plt.subplot(gs[0])
        self.ax_lines = plt.subplot(gs[1])
        self.fig.suptitle('Title of figure', fontsize=20)

        # self.the_plot = self.ax.pcolormesh(X,Y,np.zeros(X.shape), cmap=self.cmap)
        self.the_contour = self.ax_imscat.imshow(np.zeros(X.shape),cmap =self.cmap)
        self.the_line = self.ax_lines.plot(self.T,self.E, linestyle=':', color='cornflowerblue', markersize=3, marker = '8')
        # self.fig.canvas.draw()

        # placehoders for scatter plot
        self.scat = {}
        self._AntLoc = []
        self._SensorLoc = []

    def add_entropy(self,e, dt = 1):
        self.E[self.t] = e
        self.T[self.t] = self.t*dt
        self.t+=1

    @property
    def AntLoc(self):
        return self._AntLoc
    @AntLoc.setter
    def AntLoc(self,loc):
        # add the coordinate if valid, else clear list
        if loc:
            self._AntLoc.append(loc)
        else:
            self._AntLoc = []

    @property
    def SensorLoc(self,):
        return self._SensorLoc
    @SensorLoc.setter
    def SensorLoc(self,loc):
        if loc:
            self._SensorLoc.append(loc)
        else:
            self._SensorLoc = []

    def draw_contour(self,Z,):
        """ ================
            Draw the contour:
            - imshow MUCH faster than contourf
            - subsampling has little effect on draw speed
            ================"""
        # plt.cla() # free up memory (huge speed improvement)
        self.the_contour.remove()
        self.the_contour = self.ax_imscat.imshow(Z.transpose(),cmap = self.cmap, origin = 'lower')

    def draw(self):
        self.fig.canvas.draw()

    def hold_until_close(self):
        # keep the plotting window open until manually closed
        plt.show(block = True)

    def draw_scatter(self, x,y,marker = 'x', color = 'k', name = 'ant',s=80):
        if name in self.scat:
            self.scat[name].remove()
        self.scat[name] = self.ax_imscat.scatter(x,y,s=s , c=color, marker=marker)

    def draw_entropy(self):
        """ ===============
            Plot the entropy level
            =============== """
        self.ax_lines.clear()
        self.ax_lines.plot(self.T,self.E, linestyle=':', color='cornflowerblue', markersize=3, marker = '8')
        # print(self.E[np.isnan(self.E)==False])
        self.ax_lines.set_ylim(0,self.E[np.isnan(self.E)==False].max()*1.05)


def run():
    """====================
        test some things
        =================="""
    n = 100
    D = AntDomain([1000,1000], pitch =1)
    D.set_gaussian(sigma = 25)
    P = MapPlot(D.Map.X,D.Map.Y,'blue', n)
    A = Ant(start_pos = [500,500], limits = [1000,1000], speed=10, angle = 360*np.random.rand())
    i=0

    for loc in 300+np.random.rand(n,2)*600:
        i+=1
        tic = time.time()
        P.draw()
        D.local_add_pheromone(loc=loc, Q =1e3)
        D.update_pheromone()
        # P.draw_contour(D.Map.map)
        if i%5==0 or i==1:
            P.draw_contour(D.Map.map)
            P.add_entropy(D.Map.entropy, dt = 5)
            P.draw_entropy()
            # P.draw()
        A.random_step(sigma = 10)

        P.draw_scatter(A.pos.x, A.pos.y,color = 'k')
        print("Iteration {i} in {s:.4f} msec".format(i=i,s = (time.time()-tic)*1e3))
    P.hold_until_close()

if __name__ =='__main__':
    run()
