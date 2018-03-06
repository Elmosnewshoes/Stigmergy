import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import time

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
plt.ion()
class MapPlot():
    """ ===================
        do the plotting of the pheromone map
        and the scatter of ant locations
        ==================="""

    def __init__(self,X,Y,Z, area_dims = (10.,10.)):
        """ ================
            initialize the class
            ================"""
        # timing variables
        self.draw_time = 0
        self.surf_time = 0

        self.W, self.H = area_dims
        self.X = X
        self.Y = Y

        levels = MaxNLocator(nbins=15).tick_values(Z.min()+0.02,Z.max()+1)
        self.cmap = plt.get_cmap('gray_r' )
        self.norm = BoundaryNorm(levels,ncolors=self.cmap.N, clip=True)

    def set_plot(self,Z, colorscheme = cm.gray_r,):
        self.fig, self.ax1 = plt.subplots(nrows=1)
        # self.ax1 = plt.subplot(111)
        self.im = self.ax1.contourf(self.X,self.Y,Z, cmap=self.cmap, norm=self.norm)
        self.scat = self.ax1.scatter([1,2,3],[1,2,3])
        self.ax1.set_title(' title :) ')
        # plt.show()

        self.cbar = self.fig.colorbar(self.im,ax=self.ax1)
        self.fig.canvas.draw()


    def hold_until_close(self):
        # keep the plotting window open until manually closed
        plt.show(block = True)

    def draw(self, surf,scat_X=[1.], scat_Y=[1.],
             draw_bg = False, colorscheme = cm.gray_r,stepsize = 1, marker_color = 'm', marker = '>'):
        """  =================================
            Update the heatmap of the pheromone
            =================================="""
        tic = time.time()

        # check if new background contour is to be drawn
        if draw_bg:
            # remove previous background
            for coll in self.im.collections:
                coll.remove()
            #draw the new one
            levels = MaxNLocator(nbins=15).tick_values(surf.min(),surf.max())
            self.norm = BoundaryNorm(levels,ncolors=self.cmap.N, clip=True)
            self.im = self.ax1.contourf(self.X,self.Y,surf, cmap=self.cmap, norm=self.norm)
            self.cbar.set_clim()
            self.cbar.draw_all()

        #remove old scatter
        self.scat.remove()

        # draw the new scatter
        self.scat = self.ax1.scatter(scat_X,scat_Y, s=80, c=marker_color, marker=marker)
        self.surf_time = time.time()-tic
        toc = time.time()
        self.fig.canvas.draw()
        self.draw_time = time.time()-toc



def run():
    """====================
        test some things
        =================="""
    X, Y = np.meshgrid(np.arange(0,10,0.1),np.arange(0,10,0.1))
    D = mlab.bivariate_normal(X,Y, 1,1, 5,5)
    P = MapPlot(X,Y,D)
    P.set_plot(D)
    time.sleep(1)
    P.draw(D + mlab.bivariate_normal(X,Y, 1,0.5,2,2))
    time.sleep(1)
    P.draw(D + mlab.bivariate_normal(X,Y, 1,0.5,2,2) + mlab.bivariate_normal(X,Y, 1,0.5,3,3), [6, 6,7],[4,5,8],draw_bg=True)
    P.hold_until_close()


if __name__ =='__main__':
    run()
