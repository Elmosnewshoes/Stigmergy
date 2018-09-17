""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """



from ant import Ant
import numpy as np
import time


class Queen():
    """ ===============
        WORK IN PROGRESS !!!
        Manage all the agents during the simulation
        =============== """
    def __init__(self, n_agents= 1, start = 'random', dom_size = [1000,1000],):
        self.ant_list = []
        self.n_agents = n_agents
        self.start = start
        self.dom_size = dom_size

    def positions(self,):
        """ ===============
            Return an np array of all the positions of the ant
            [[x1, y1],[x2,y2],...[xn,yn]]
            =============== """
        return np.matrix([ant.pos.vec for ant in self.ant_list])

    def sensor_positions(self,):
        """ ===============
            like self.positions for the sensor locations
            return 2 matrices, left and right vector
            Return an np array of all the positions of the ant
            [[x1, y1],[x2,y2],...[xn,yn]]
            =============== """
        return np.matrix([ant.sensors['left'].vec
                          for ant in self.ant_list]), np.matrix(
                              [ant.sensors['right'].vec
                              for ant in self.ant_list])

    def deploy(self, start = 'random', v_max = 1e9):
        """ ===============
            Deploy a number of ants according to the situation specified at
            self.start
            =============== """
        v_max = 10
        self.ant_list = [ Ant(start_pos = [1,1], ant_id = i, v_max = v_max, limits = self.dom_size)
         for i in range(self.n_agents)]

def run():
    X = Queen(n_agents = 10)
    X.deploy()
    tic = time.time()
    print(X.positions())
    print("Position update took {:.4f} msec".format((time.time()-tic)*1e3))
    x,y = X.sensor_positions()
    print(x)
    print(y)
if __name__ == '__main__':
    run()
