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

        # placeholders for position of the sensors and ants
        self.ants_pos_x = []
        self.ants_pos_y = []
        self.ants_sens_left_x = []
        self.ants_sens_left_y = []
        self.ants_sens_right_x = []
        self.ants_sens_right_y = []

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
        for i in range(self.n_agents):
            with Ant(start_pos = [1,1], ant_id = i, v_max = v_max, limits = self.dom_size) as A:
                self.ant_list.append(A)
                self.ants_pos_x.append(A.pos.x)
                self.ants_pos_y.append(A.pos.y)
                self.ants_sens_left_x.append(A.sensors['left'].x)
                self.ants_sens_left_y.append(A.sensors['left'].y)
                self.ants_sens_right_x.append(A.sensors['right'].x)
                self.ants_sens_right_y.append(A.sensors['right'].y)

        # self.ant_list = [ Ant(start_pos = [1,1], ant_id = i, v_max = v_max, limits = self.dom_size)
                        # for i in range(self.n_agents)]

    def gradient_step(self, Q,theta_max=360,dt=1, SNR = 0, gain = 1):
        for i in range(self.n_agents):
            with self.ant_list[i] as ant:
                ant.gradient_step([1,1],theta_max,dt,SNR,gain)


def run():
    X = Queen(n_agents = 10)
    X.deploy()
    tic = time.time()
    print(X.positions())
    print("Position update took {:.4f} msec".format((time.time()-tic)*1e3))
    # x,y = X.sensor_positions()
    X.gradient_step(Q=0)
    print(X.ant_list[1].pos.vec)
if __name__ == '__main__':
    run()
