# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Visualization of theANT3000 simulator.
# Modification from: https://matplotlib.org/examples/animation/subplots.html
# =======================================


from cythonic.core.sim_player import SimPlayer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from matplotlib import cm
import matplotlib.colors as colors

from mpl_toolkits.axes_grid1 import make_axes_locatable
from cythonic.plugins.db_controller import db_controller
from cythonic.plugins.db_path import db_path
from cythonic.core.sim_player import extract_settings

def check_sim(sim_id, dbpath = db_path(), dbname='stigmergy.db'):
    db = db_controller(dbpath, dbname)
    q1 = f"SELECT count(ID) as counted FROM sim WHERE sim.id = {sim_id}"
    q2 = f"SELECT IFNULL(steps_recorded,0)steps_recorded FROM sim WHERE sim.id = {sim_id}"
    if extract_settings(*db.return_all(q1))['counted']==0:
        return -1 # sim id does not exist in database
    else:
        return int(extract_settings(*db.return_all(q2))['steps_recorded'])

cmaps = {'blue': 'PuBu',
         'grey_reverse': 'Greys_r',
         'grey': 'Greys',
         'plasma': 'plasma'
         }
class SubplotAnimation(animation.TimedAnimation):
    def __init__(self, sim_id = 4872,db_name = 'stigmergy.db', colormap = 'plasma', store_interval = [], path = '', name = ''):
        self.status = check_sim(sim_id, dbname = db_name)
        self.store_interval = store_interval
        self.recording = False
        if len(self.store_interval) >0:
            self.recording = True
        self.path = path
        self.name = name
        if self.status >= 1:
            self.new(sim_id, db_name,colormap) #continue
        elif self.status == 0:
            self.simple_plot(sim_id, db_name) #  no steps/live sim but only results
        else:
            pass # abort

    def simple_plot(self, sim_id, db_name):
        qry = f"SELECT entropy_vec, scorecard, step_vec from results where sim_id = {sim_id}"
        data, headers = db_controller(db_path(), db_name).return_all(qry)
        H, Y, K = [eval(x) for x in data[0]] #extract results

        fig = plt.figure(figsize = (18,9))
        ax_entropy = fig.add_subplot(2,1,1)
        ax_score = fig.add_subplot(2,1,2)
        ax_entropy.plot(K,H)
        ax_score.plot(K,Y)
        ax_entropy.set_xlabel('k')
        ax_entropy.set_ylabel('H')
        ax_entropy.set_ylim(0, max(H)*1.1)
        ax_score.set_xlabel('k')
        ax_score.set_ylabel('No. Nest returns')
        ax_score.set_ylim(0, max(Y)*1.1)

        plt.show()


    def new(self,sim_id, db_name, colormap):
        self.replays = 0 # flag to see if a replay is being played
        self.player = SimPlayer(sim_id, db_name)
        self.player.get_steps() # fetch all ant movements from database
        self.player.get_results() # fetch the result summary vectors from database

        fig = plt.figure(figsize=(18, 9))
        self.f = fig
        # ax1 = fig.add_subplot(1, 2, 1)
        ax_map = fig.add_subplot(1,2,1)

        # self.k = self.player.K_vec
        self.t = self.player.T_vec
        self.h = self.player.H_vec
        self.y = self.player.score_vec

        self.imshow_opts = {'cmap':plt.get_cmap(cmaps[colormap]),
                               'extent':[0,int(self.player.xlim),
                                         0,int(self.player.ylim)],
                               'vmin':0,
                               'origin':'bottom'}
        if self.player.global_max > 0.:
            self.imshow_opts['vmax'] = 1.25 * self.player.global_max
        else:
            self.imshow_opts['vmax'] = 3
        self.imshow_opts['norm']= colors.PowerNorm(gamma=1. / 4.)
        Z = self.player.map
        self.map = ax_map.imshow(Z, interpolation='None',**self.imshow_opts)
        fig.colorbar(self.map,orientation="horizontal")
        ax_entropy = fig.add_subplot(2, 2, 2)
        ax_score = fig.add_subplot(2, 2, 4)
        # self.ants = ax_map.scatter([], [],marker = 'o', s=10, c='k', alpha=1.)
        self.ants = ax_map.scatter([],[],marker = 'o',facecolors='white', edgecolors='black', s = 10, alpha = 1.)
        self.left = ax_map.scatter([], [],marker = '*', s=10, c='k', alpha=1.)
        self.right = ax_map.scatter([], [],marker = '*', s=10, c='k', alpha=1.)
        self.dropper = ax_map.scatter([], [], marker = '*', s=10, c = 'gray', alpha=1.)
        self.nest = ax_map.scatter([], [],marker = '.', s=10, c='k', alpha=1.)
        self.food = ax_map.scatter([], [],marker = '.', s=10, c='k', alpha=1.)
        ax_map.set_xlabel('x')
        ax_map.set_ylabel('y')
        ax_map.set_title('Pheromone map')

        ax_entropy.set_xlabel('t')
        ax_entropy.set_ylabel('H')
        self.line_H = Line2D([], [], color='black')
        self.line_H_future  = Line2D([], [], color='blue', linestyle = '--')
        ax_entropy.add_line(self.line_H)
        ax_entropy.add_line(self.line_H_future)
        # ax_entropy.set_xlim(0, self.player.steps)
        ax_entropy.set_xlim(0,max(self.player.T_vec))
        ax_entropy.set_ylim(0, max(self.player.H_vec)+1)

        ax_score.set_xlabel('t')
        ax_score.set_ylabel('score')
        self.line_score = Line2D([], [], color='black')
        self.line_score_future = Line2D([], [], color='blue',linestyle = '--')
        ax_score.add_line(self.line_score)
        ax_score.add_line(self.line_score_future)
        # ax_score.set_xlim(0, self.player.steps)
        ax_score.set_xlim(0,max(self.player.T_vec))
        ax_score.set_ylim(0, max([1.1*max(self.player.score_vec),1]))

        animation.TimedAnimation.__init__(self, fig, interval=10, blit=True,
                                          repeat = True, repeat_delay=None)


    def _draw_frame(self, framedata):
        self.player.next()
        # i = framedata
        if self.player.current_step in self.store_interval:
            print('recording!!')
            "store a copy of the pheromone map"
            name = self.name + f"i{self.player.current_step}"
            self.player.store_map(self.path,name)

        self.map.set_data(self.player.map)
        self.ants.set_offsets(self.player.pos)
        self.dropper.set_offsets(self.player.drop)
        self.left.set_offsets(self.player.lft)
        self.right.set_offsets(self.player.rght)
        self.line_H.set_data(self.player.T,self.player.H)
        self.line_H_future.set_data(self.player.T_future,self.player.H_future)
        self.line_score.set_data(self.player.T,self.player.score)
        self.line_score_future.set_data(self.player.T_future,self.player.score_future)
        self._drawn_artists = [self.map,self.ants,self.dropper, self.nest,self.food, self.left, self.right, self.line_H, self.line_score, self.line_score_future, self.line_H_future]

    def new_frame_seq(self):
        return iter(range(self.player.steps))

    def _init_draw(self):
        " this is called twice at start, then once at each iteration "
        if self.replays > 1:
            self.player.renew()
        else:
            self.replays +=1
        lines = [self.line_H, self.line_H_future, self.line_score_future, self.line_score]
        self.map.set_data( self.player.map)
        self.ants.set_offsets(self.player.pos)
        self.nest.set_offsets(self.player.nest)
        self.food.set_offsets(self.player.food)
        self.left.set_offsets(self.player.lft)
        self.right.set_offsets(self.player.rght)
        self.dropper.set_offsets(self.player.drop)
        for l in lines:
            l.set_data([], [])

def show_plot(id, colormap = 'plasma'):
    ani = SubplotAnimation(sim_id = id, colormap = colormap)
    if ani.status > 0:
        plt.show()
    return ani.status

def store_map(id, steps, colormap='plasma'):
    " store a copy of the map at specified steps"
    id = id
    path = db_path()+'maps/'
    name = f'{id}_'
    print(path)
    ani = SubplotAnimation(sim_id = id, path=path, name = name,store_interval = steps, colormap = colormap)
    plt.show()


if __name__=='__main__':
    ani = SubplotAnimation()
    # ani.save('test_sub.mp4')
    plt.show()
