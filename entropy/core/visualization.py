import numpy as np
from matplotlib import cm, gridspec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from core.plugins.helper_classes import point, loc

cmaps = {'blue': 'PuBu',
         'grey_reverse': 'Greys_r',
         'grey': 'Greys',
         'plasma': 'plasma'
         }
class Plotter():
    " base plot class (not interactive) "
    def __init__(self, M, colormap = 'blue', figsize = (10,6), shown='all'):
        self.stigmergy_opts = {'cmap':plt.get_cmap(cmaps[colormap]),
                               'extent':[0,np.array(M.mesh_x).max().copy(),
                                         0,np.array(M.mesh_y).max().copy()],
                               'origin':'bottom'}
        if shown=='all':
            self.fig = plt.figure(figsize =figsize, constrained_layout = True)
            self.gs = gridspec.GridSpec(1,3,width_ratios=[.1,3,.9], figure = self.fig) #2 plots in a single figure
            self.ax_stigmergy = plt.subplot(self.gs[1])
            self.ax_entropy = plt.subplot(self.gs[2])
        elif shown =='stigmergy':
            self.fig, self.ax_stigmergy = plt.subplots(figsize =figsize, constrained_layout = True)
        self.stigmergy_limits(np.array(M.mesh_x).max(),np.array(M.mesh_y).max())
        self.scat = {} #hold scatters

    def stigmergy_limits(self,x_max, y_max):
        self.ax_stigmergy.set_xticks(np.arange(0, x_max, 250));
        self.ax_stigmergy.set_yticks(np.arange(0, y_max, 250));
        self.ax_stigmergy.set_xlim((0,x_max))
        self.ax_stigmergy.set_ylim((0,y_max))

    def draw_cb(self):
        self.ax_cb = plt.subplot(self.gs[0])
        fig.colorbar(self.stigmergy,cax = self.ax_cb,orientation = 'vertical',pad=.1)

    def draw_stigmergy(self,Z):
        try:
            self.stigmergy.remove()
        except:
            pass
        self.stigmergy = self.ax_stigmergy.imshow(Z,vmin=0,**self.stigmergy_opts)


    def draw_entropy(self,H, **kwargs):
        " Draw line plot of entropy H "
        try:
             self.entropy.clear()
        except:
            pass
        if not 't' in kwargs:
            t = np.arange(len(H))
        else:
            t=kwargs['t']
        self.entropy = self.ax_entropy.plot(t,H, linestyle=':', color='cornflowerblue', markersize=3, marker = '8')
        self.ax_entropy.set_ylim(0,H.max()*1.05)

    def show(self):
        plt.show()

    def save(self,path, dpi = 50):
        self.fig.savefig(path,bbox_inches = 'tight', format ='eps', dpi = dpi)

    def set_subtitles(self):
        self.ax_stigmergy.set_title('Pheromone volume')
        self.ax_entropy.set_title('entropy')

    def draw_scatter(self,x,y,marker='x',color='k',name='ant',s=80):
        if name in self.scat:
            self.scat[name].remove()
        self.scat[name] = self.ax_stigmergy.scatter(x,y,s=s,c=color,marker=marker)

    def set_labels(self, target = ''):
        if target == 'entropy' or target == '':
            self.ax_entropy.set_xlabel('time (s)')
            self.ax_entropy.set_ylabel('Entropy (H)')
        if target == 'stigmergy' or target == '':
            self.ax_stigmergy.set_xlabel('x1 [mm]')
            self.ax_stigmergy.set_ylabel('x2 [mm]')

class StigmergyPlot(Plotter):
    " interactive plotter "
    def __init__(self, Map, colormap = 'blue', figsize = (10,6), shown = 'all'):
        plt.ion() # make interactive
        super().__init__(M =Map, colormap = colormap, figsize = figsize, shown=shown)
        self.ant_loc = np.empty((0,2))

    def append_scatter(self,arr, a):
        """ pnt as point tuple/class """
        return np.append(arr, np.resize(a.vec,(1,2)),axis=0)

    def draw(self):
        self.fig.canvas.draw()

    def hold_until_close(self):
        plt.show(block = True)
