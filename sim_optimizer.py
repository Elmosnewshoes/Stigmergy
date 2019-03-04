# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Simple ACO ( https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms )
#   script to finetune some simulation parameters for the theANT3000 sim
# =======================================

from cythonic.plugins.aco_optimizer import optimizer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from matplotlib import cm
import time
from cythonic.plugins.aco_optimizer import optimizer

def test_fun(x,y,*args):
    return x**2+y**2+1

class SubplotAnimation(animation.TimedAnimation):
    def __init__(self, fun, k, beta, n_ants, pars_dict, q, tau, method, neighbours, steps):
        self.steps= steps #max number of iterations
        self.optimizer = optimizer(fun,k,beta,n_ants)
        self.stepargs = {'q':q,'tau':tau,'method':method, 'neighbours' : neighbours}
        fig = plt.figure(figsize = (12,6))
        ax = []
        self.plts = []

        " fill the route list "
        for key, value in pars_dict.items():
            self.optimizer.add_par(value,key)

        " loop over the fresh route list and add plots "
        for i in range(self.optimizer.segments):
            ax.append( fig.add_subplot(self.optimizer.segments,2,2*(i+1)-1))

            self.plts.append(ax[i].matshow([self.optimizer.fun_pars[i].weights,
                                            self.optimizer.fun_pars[i].weights],
                          vmin=0, origin = 'bottom',
                          extent = [0,self.optimizer.fun_pars[i].n,0,1]))
            ax[i].set_xlabel(self.optimizer.fun_pars[i].name)
        self.ax_linescat = fig.add_subplot(1, 2, 2)
        self.line = Line2D([],[], color = 'black')
        self.ax_linescat.add_line(self.line)
        self.ax_linescat.set_xlim(-.5,self.steps+.5)
        self.scat = self.ax_linescat.scatter([],[],marker = '.', s = 5, c = 'b', alpha = .5)
        animation.TimedAnimation.__init__(self, fig, interval=0.1, blit=True,
                                                  repeat = False, repeat_delay=None)
        #

    def _draw_frame(self, framedata):
        self.optimizer.step(**self.stepargs)
        i = framedata
        XY = np.vstack([self.optimizer.t,self.optimizer.scores]).transpose()
        self.scat.set_offsets(XY)
        self.ax_linescat.set_ylim(min(XY[:,1])*1.1, max(XY[:,1])*1.1)
        self.line.set_data(range(i+1),self.optimizer.cost)
        i = 0
        for subplot in self.plts:
            subplot.set_data([self.optimizer.fun_pars[i].weights,
                                self.optimizer.fun_pars[i].weights])
            i+=1
        l = self.plts.copy()
        l.append(self.line)
        l.append(self.scat)

        self._drawn_artists = l

    def new_frame_seq(self):
        return iter(range(self.steps))

    def _init_draw(self):
        " this is called twice at start, then once at each iteration "
        # lines = [self.line_H, self.line_score]
        i = 0
        for subplot in self.plts:
            subplot.set_data([self.optimizer.fun_pars[i].weights,
                                self.optimizer.fun_pars[i].weights])
            i+=1
from cythonic.sim_wrapper import recorder
from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict

initiator = 'ACO no.2'

def sim_fun(q, gain, noise_gain,sens_offset, covariance):
    domain_dict = {
        'size': [2000,1500],
        'pitch': 10,
        'nest_loc': [500,750],
        'nest_rad': 150,
        'food_loc': [1500,750],
        'food_rad': 150,
        'target_pheromone': 1.
    }
    sim_dict['steps'] = 1000
    sim_dict['n_agents'] = 80
    domain_dict['pitch']=10
    deposit_dict['q'] = q # originally 1000
    ant_dict['gain'] = gain # originally .5
    ant_dict['noise_gain']= noise_gain # originally 2
    gauss_dict['covariance']= covariance # originally 20
    ant_dict['sens_offset'] = sens_offset # originally 45
    queen_dict['default_speed'] = 125
    sim_dict['evap_rate'] = .97
    queen_dict['noise_type'] = 'telegraph'
    queen_dict['noise_parameter'] = 10 #higher means direction changes last longer with telegraph noise
    ant_dict['deposit_fun'] = 'exp_decay'
    deposit_dict['beta'] = .01
    record = False
    r = 0
    for i in range(3):
        sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict)
        result = sim_recorder.time_full_sim(record = record, deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = 500, initiator = initiator)
        r+= result['nestcount']
    return -1*r/3

if __name__=='__main__':
    k = .5
    beta = 1.6
    q = 1.5
    tau = .8
    n_ants = 35
    method = 'elitist'
    neighbours = True
    steps = 25



    x_range = np.arange(-5,5,0.25)
    y_range = np.arange(-50,50,1)

    pars = {'q': np.array([1500,2000,2500,3000, 5000, 7500, 10000]),
            'gain': np.array([0.1,0.2,0.3,0.5,0.75,1,1.25,1.5,2]),
            'noise_gain': np.arange(0.25,5,0.25),
            'sens_offset': np.array([30,35,40,45, 50, 60]),
            'covariance': np.array([20,25,30,35,40,50,60])}
    plotter = SubplotAnimation(sim_fun, k, beta, n_ants, pars, q, tau, method, neighbours, steps)
    plt.show()
    plotter.optimizer.postrun()
