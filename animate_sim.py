"""
=================
Animated subplots
=================

Modification from: https://matplotlib.org/examples/animation/subplots.html

"""



from cythonic.core.sim_player import SimPlayer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from matplotlib import cm

from mpl_toolkits.axes_grid1 import make_axes_locatable
cmaps = {'blue': 'PuBu',
         'grey_reverse': 'Greys_r',
         'grey': 'Greys',
         'plasma': 'plasma'
         }
class SubplotAnimation(animation.TimedAnimation):
    def __init__(self, sim_id = 159,db_name = 'stigmergy.db', colormap = 'plasma'):

        self.replays = 0 # flag to see if a replay is being played
        self.player = SimPlayer(sim_id, db_name)
        self.player.get_steps() # fetch all ant movements from database
        self.player.get_results() # fetch the result summary vectors from database

        fig = plt.figure(figsize=(18, 9))
        self.f = fig
        # ax1 = fig.add_subplot(1, 2, 1)
        ax_map = fig.add_subplot(1,2,1)
        ax_entropy = fig.add_subplot(2, 2, 2)
        ax_score = fig.add_subplot(2, 2, 4)

        self.k = self.player.K_vec
        self.h = self.player.H_vec
        self.y = self.player.score_vec

        self.imshow_opts = {'cmap':plt.get_cmap(cmaps[colormap]),
                               'extent':[0,int(self.player.xlim),
                                         0,int(self.player.ylim)],
                               'vmin':0,
                               'origin':'bottom'}
        Z = self.player.map
        self.map = ax_map.imshow(Z, interpolation='None',**self.imshow_opts)
        self.ants = ax_map.scatter([], [],marker = 'o', s=10, c='k', alpha=1.)
        self.left = ax_map.scatter([], [],marker = '*', s=10, c='k', alpha=1.)
        self.right = ax_map.scatter([], [],marker = '*', s=10, c='k', alpha=1.)
        self.nest = ax_map.scatter([], [],marker = '.', s=10, c='k', alpha=1.)
        self.food = ax_map.scatter([], [],marker = '.', s=10, c='k', alpha=1.)
        ax_map.set_xlabel('x')
        ax_map.set_ylabel('y')
        ax_map.set_title('Pheromone map')

        ax_entropy.set_xlabel('k')
        ax_entropy.set_ylabel('H')
        self.line_H = Line2D([], [], color='black')
        ax_entropy.add_line(self.line_H)
        ax_entropy.set_xlim(0, self.player.steps)
        ax_entropy.set_ylim(0, max(self.player.H_vec)+1)

        ax_score.set_xlabel('k')
        ax_score.set_ylabel('score')
        self.line_score = Line2D([], [], color='black')
        ax_score.add_line(self.line_score)
        ax_score.set_xlim(0, self.player.steps)
        ax_score.set_ylim(0, max([1.1*max(self.player.score_vec),1]))

        animation.TimedAnimation.__init__(self, fig, interval=10, blit=True,
                                          repeat = True, repeat_delay=None)


    def _draw_frame(self, framedata):
        self.player.next()
        # i = framedata
        self.map.set_data(self.player.map)
        self.ants.set_offsets(self.player.pos)
        self.left.set_offsets(self.player.lft)
        self.right.set_offsets(self.player.rght)
        self.line_H.set_data(self.player.K,self.player.H)
        self.line_score.set_data(self.player.K,self.player.score)
        self._drawn_artists = [self.map,self.ants,self.nest,self.food, self.left, self.right, self.line_H, self.line_score]
    def new_frame_seq(self):
        return iter(range(self.player.steps))

    def _init_draw(self):
        " this is called twice at start, then once at each iteration "
        if self.replays > 1:
            self.player.renew()
        else:
            self.replays +=1
        lines = [self.line_H, self.line_score]
        self.map.set_data( self.player.map)
        self.ants.set_offsets(self.player.pos)
        self.nest.set_offsets(self.player.nest)
        self.food.set_offsets(self.player.food)
        self.left.set_offsets(self.player.lft)
        self.right.set_offsets(self.player.rght)
        for l in lines:
            l.set_data([], [])

def show_plot(id, colormap = 'plasma'):
    ani = SubplotAnimation(sim_id = id, colormap = colormap)
    plt.show()

if __name__=='__main__':
    ani = SubplotAnimation()
    # ani.save('test_sub.mp4')
    plt.show()
    print(f"Max of domain: {ani.player.max}")
