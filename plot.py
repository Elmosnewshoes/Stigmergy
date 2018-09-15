import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import time
from domain import AntDomain

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
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

    def __init__(self,X,Y, colormap = 'blue'):
        """ ================
            initialize the class
            ================"""
        # timing variables
        self.draw_time = 0
        self.surf_time = 0

        # local copy of meshgrid
        self.X = X
        self.Y = Y

        # define the colormap to use
        self.cmap = plt.get_cmap(cmaps['blue'] )

        # define the plot variables
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        # self.the_plot = self.ax.pcolormesh(X,Y,np.zeros(X.shape), cmap=self.cmap)
        self.the_plot = self.ax.imshow(np.zeros(X.shape),cmap =self.cmap)
        self.fig.canvas.draw()

        # placehoders for scatter plot
        self._AntLoc = []
        self._SensorLoc = []

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
        plt.cla() # free up memory (huge speed improvement)
        self.the_plot = self.ax.imshow(Z.transpose(),cmap = self.cmap, origin = 'lower')
        self.fig.canvas.draw()

    def hold_until_close(self):
        # keep the plotting window open until manually closed
        plt.show(block = True)

    def add_scatter(self,loc,*sensor_loc):
        """ ================
            Add scatter

    # def set_plot(self,Z):
    #     self.fig, self.ax1 = plt.subplots(nrows=1)
    #     # self.ax1 = plt.subplot(111)
    #     self.im = self.ax1.contourf(self.X,self.Y,Z, cmap=self.cmap, norm=self.norm)
    #     self.scat = self.ax1.scatter([1,2,3],[1,2,3])
    #     self.ax1.set_title(' title :) ')
    #     # plt.show()
    #
    #     self.cbar = self.fig.colorbar(self.im,ax=self.ax1)
    #     self.fig.canvas.draw()
    #
    #
    # def hold_until_close(self):
    #     # keep the plotting window open until manually closed
    #     plt.show(block = True)
    #
    # def draw(self, surf,scat_X=[1.], scat_Y=[1.],
    #          draw_bg = False, colorscheme = cm.gray_r,stepsize = 1, marker_color = 'm', marker = '>'):
    #     """  =================================
    #         Update the heatmap of the pheromone
    #         =================================="""
    #     tic = time.time()
    #
    #     # check if new background contour is to be drawn
    #     if draw_bg:
    #         # remove previous background
    #         for coll in self.im.collections:
    #             coll.remove()
    #         #draw the new one
    #         levels = MaxNLocator(nbins=15).tick_values(surf.min(),surf.max())
    #         self.norm = BoundaryNorm(levels,ncolors=self.cmap.N, clip=True)
    #         self.im = self.ax1.contourf(self.X,self.Y,surf, cmap=self.cmap, norm=self.norm)
    #         # self.cbar.set_clim()
    #         # self.cbar.draw_all()
    #         self.cbar.update_normal(self.im)
    #         self.cbar.draw_all()
    #         # self.fig.colorbar(self.im)
    #
    #     #remove old scatter
    #     self.scat.remove()
    #
    #     # draw the new scatter
    #     self.scat = self.ax1.scatter(scat_X,scat_Y, s=80, c=marker_color, marker=marker)
    #     self.surf_time = time.time()-tic
    #     toc = time.time()
    #     self.fig.canvas.draw()
    #     self.draw_time = time.time()-toc



def run():
    """====================
        test some things
        =================="""
    # X, Y = np.meshgrid(np.arange(0,10,0.1),np.arange(0,10,0.1))
    # D = mlab.bivariate_normal(X,Y, 1,1, 5,5)
    # P = MapPlot(X,Y,D)
    # P.set_plot(D)
    # time.sleep(1)
    # P.draw(D + mlab.bivariate_normal(X,Y, 1,0.5,2,2))
    # time.sleep(1)
    # P.draw(D + mlab.bivariate_normal(X,Y, 1,0.5,2,2) + mlab.bivariate_normal(X,Y, 1,0.5,3,3), [6, 6,7],[4,5,8],draw_bg=True)
    # P.hold_until_close()
    D = AntDomain([1000,1000], pitch =1)
    D.set_gaussian(sigma = 25)
    P = MapPlot(D.Map.X,D.Map.Y,'blue')
    i=0
    for loc in 300+np.random.rand(1500,2)*600:
        i+=1
        tic = time.time()
        D.local_add_pheromone(loc=loc, Q =1e3)
        D.update_pheromone()
        # P.draw_contour(D.Map.map)
        if i%5==0:
            P.draw_contour(D.Map.map)
        print("Iteration {i} in {s:.4f} msec".format(i=i,s = (time.time()-tic)*1e3))
    P.hold_until_close()

if __name__ =='__main__':
    run()
