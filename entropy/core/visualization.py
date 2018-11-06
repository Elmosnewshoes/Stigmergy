import numpy as np
from matplotlib import cm, gridspec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from plugins.helper_classes import point, loc

cmaps = {'blue': 'PuBu',
         'grey_reverse': 'grey_r',
         }

class StigmergyPlot:
    def __init__(self,Map, colormap = 'blue', n = 10,pitch=1):
        """ Setup, Map instance of MeshMap,
         colormap and size of time steps vector"""
        self.mesh_x = Map.mesh_x #meshgrid coordinates
        self.mesh_y = Map.mesh_y #idem

        self.time_vec = np.arange(n)
        self.entropy_vec = np.zeros((n,1))

        # self.cmap = plt.get_cmap(cmaps['blue'])
        plt.ion() # make interactive
        self.fig = plt.figure(figsize=(8,6))
        self.ax = self.fig.gca()

        gs = gridspec.GridSpec(1,2,width_ratios=[3,1]) #2 plots in a single figure
        self.ax_stigmergy = plt.subplot(gs[0])
        self.ax_entropy = plt.subplot(gs[1])
        self.fig.suptitle('Note to self, fix title', fontsize = 20)

        self.stigmergy_opts = {'cmap':plt.get_cmap(cmaps['blue']),
                               'extent':[0,self.mesh_x.max().copy(),
                                         0,self.mesh_y.max().copy()],
                               'origin':'bottom'}
        self.stigmergy = self.ax_stigmergy.imshow(np.zeros(self.mesh_x.shape),
                                                  **self.stigmergy_opts)
        self.ax_stigmergy.set_xticks(np.arange(0, self.mesh_x.max(), 250));
        self.ax_stigmergy.set_yticks(np.arange(0, self.mesh_y.max(), 250));
        self.ax_stigmergy.set_xlim((0,self.mesh_x.max()))
        self.ax_stigmergy.set_ylim((0,self.mesh_y.max()))
        self.entropy = self.ax_entropy.plot(self.time_vec, self.entropy_vec)
        # self.ax_stigmergy.invert_yaxis()

        #placeholders for the scatter plot of ants
        self.scat = {} #hold scatters for ant and sensor locations
        self.ant_loc = np.empty((0,2))

    def append_scatter(self,arr, a):
        """ pnt as point tuple/class """
        return np.append(arr, np.resize(a.vec,(1,2)),axis=0)

    def draw_stigmergy(self,Z):
        """ Use imshow, much faster than contourf,
            subsampling has little effect on draw speed """
        self.stigmergy.remove()
        self.stigmergy = self.ax_stigmergy.imshow(Z,
                                                  **self.stigmergy_opts)

    def draw_scatter(self,x,y,marker='x',color='k',name='ant',s=80):
       if name in self.scat:
           self.scat[name].remove()
       self.scat[name] = self.ax_stigmergy.scatter(x,y,s=s,c=color,marker=marker)

    def draw_entropy(self,H):
       " Draw line plot of entropy H "
       self.entropy.clear()
       self.entropy_vec = H
       if len(H) != len(self.time_vec):
           self.time_vec = np.arange(len(H))
       self.entropy = self.ax_entropy.plot(self.time_vec,H, linestyle=':', color='cornflowerblue', markersize=3, marker = '8')
        # self.ax_lines.set_ylim(0,self.E[np.isnan(self.E)==False].max()*1.05)

    def draw(self):
        self.fig.canvas.draw()

    def hold_until_close(self):
        plt.show(block = True)

def run_plot():
    from domain import Domain
    from ant import Ant, lin_fun
    domain_dict = {'size': [1000,1000],
                   'pitch': 2,
                   'nest':{'location': [250,500],'radius':50},
                   'food':{'location': [750,500],'radius':50},
                   'start_concentration':1}
    n = 500
    D = Domain(**domain_dict)
    D.Gaussian = D.init_gaussian(sigma=5,significancy =1e2)
    P = StigmergyPlot(Map=D.Map, n=n,pitch=D.pitch)


    ant_settings = {'start_pos': [500,100],
                    'angle': 45,
                    'speed': 20,
                    'limits': [1000,1000],
                    'l': 10,
                    'antenna_offset': 30}
    A = Ant(**ant_settings)
    for i in range(n+1):

        ant_loc = A.pos
        left = A.sensors['left']
        right = A.sensors['right']
        D.local_add_pheromone(ant_loc,1e6)
        D.update_pheromone()

        P.draw_scatter(ant_loc.x,ant_loc.y)
        P.draw_scatter(left.x,left.y, name='left')
        P.draw_scatter(right.x,right.y, name ='right')
        if i%10 == 0:
            P.draw_stigmergy(D.Map.map)
            P.draw()
        Q = [D.probe_pheromone(A.sensors['left']),
             D.probe_pheromone(A.sensors['right'])]
        A.observe_pheromone(lin_fun,Q)
        A.step(dt=1)

    P.hold_until_close()


if __name__=='__main__':
    run_plot()
