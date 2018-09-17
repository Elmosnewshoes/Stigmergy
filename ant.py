""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

import numpy as np
import time
from small_functions import T_matrix, Point


class Ant():
    """ ===========================
        The main agents/actors in the simulation
        =========================== """
    # start_pos (x,y) in mm
    # limits (x_lim, y_lim) in mm

    def __init__(self, start_pos = [1,1], limits = [10,10], ant_id =0, speed=0,
                 angle=0, v_max = 1e9, activation = 'linear'):
        """  =================================
            Initialize the class
            ================================== """
        # give the agent an ID (int)
        self.ID = ant_id

        # set the start coordinates and domain limits
        self.pos = Point(start_pos) #ant (starting) position in mm
        self._azimuth = angle #azimuth angle [degrees] counterclockwise, base: x-axis
        self.limits = Point(limits)  #domain limits in mm

        # ant physical properties
        self.l = 30 #length in mm (distance between CoM and sensors)
        self.antenna_offset = 30 #angle [degrees] between centerline and antenna from the base of the antenna
        self.sensors = {'left':Point([0,0]), #position of the sensors (absolute)
                   'right': Point([0,0])}
        self.set_sensor_position()

        # assign private RNG
        self.gen = np.random.RandomState()

        # set the physical state of the ant
        self.v_max = v_max
        self.v = speed

        print("Booted up agent {}".format(int(self.ID)))

        # Some settings regarding boundary and food/nest awareness
        self.foodbound = True
        self.out_of_bounds = False

    def reverse(self):
        self.azimuth = self.azimuth+180

    @property
    def sens_loc(self):
        return [self.sensors['left'].vec, self.sensors['right'].vec]

    @property # handle setting of azimuth with restrictions
    def azimuth(self):
        return self._azimuth
    @azimuth.setter
    def azimuth(self, azimuth): # bound azimuth between 0 and 360
        if azimuth >= 360:
            self._azimuth = azimuth-360
        elif azimuth < 0:
            self._azimuth = azimuth+360
        else:
            self._azimuth = azimuth

    def calc_position(self,dt):
        """ ============================
            Calculate the Ant position based on the current speed and orientation
            follow the wall when in danger of leaving the domain
            toggle foodbound and out_of_bounds if necessary
            ============================ """
        new_pos = np.dot(dt,self.pos.vec
                         + np.dot(self.v,[1,0])*T_matrix(self.azimuth).transpose())

        # compensate for boundaries
        self.pos.vec = np.maximum(new_pos,[0,0]) #lower bounds
        self.pos.vec = np.minimum(self.pos.vec,self.limits.vec) #upper bounds

        # check boundaries
        if (min(self.pos.vec) <1e-3
            or self.pos.x >= self.limits.x-1e-3
            or self.pos.y >=self.limits.y-1e-3):
            self.out_of_bounds = True
        else:
            self.out_of_bounds = False

    def set_sensor_position(self):
        """ ============================
            set the absolute location of the sensors based on the ants' properties
            and orientation/position
            ============================ """
        self.sensors['left'].vec = (self.pos.vec
                                    + np.dot(self.l,[1,0])
                                    *T_matrix(self.azimuth
                                              + self.antenna_offset).transpose())
        self.sensors['right'].vec = (self.pos.vec
                                     + np.dot(self.l,[1,0])
                                     *T_matrix(self.azimuth
                                               - self.antenna_offset).transpose())

    def observed_pheromone(self,Q, activation = 'linear', a= 1, c = 1, **kwargs):
        """ ============================
            Transform the absolute quantity of pheromone to something
            observed by the ant through a (nonlinear) transformation
            Q = pheromone quantity
            c = breakpoint location in case of sigmoid function
            a = steepness of sigmoid curve
            ============================ """
        # === preprocessing ==
        if 'gain' in kwargs:
            gain = kwargs['gain']
        else:
            gain = 1
        if type(Q) is list:
            Q = np.matrix(Q) #list to numpy matrix

        # == return value ==
        if activation == 'linear':
            return gain*Q
        elif activation == 'sigmoid':
            return gain/(1+np.exp(-np.dot(a,(Q-c))))
        else:
            return Q

    def gradient_step(self,Q,theta_max=360,dt=1, SNR = 0, gain = 1):
        """ ============================
            Take a step towards the direction with the highest amount of
            (observed) pheromone
            Q = observed pheromone quantity per sensor [L, R] (normalized)
            theta_max = max degrees/second turn
            dt = timestep
            SNR = signal to noise ratio
            ============================ """
        # todo: add noise, update: done!
        # todo2: speed based on pheromon quantity

        if type(Q) is list:
            Q = np.matrix(Q)
        diff = gain*(Q[0,0]-Q[0,1]) #difference between left and right: -1<=diff<=1

        #update orientation based on pheromone
        self.azimuth += (diff + SNR*2*(np.random.rand()-0.5)) * theta_max

        # print("Q_left: {:.4f}, Q_right: {:.4f} -> d_theta: {:.4f}".
        #       format(Q[0,0], Q[0,1],diff*theta_max))

        #perform step in new direction
        self.calc_position(dt=dt)
        self.set_sensor_position()

    def random_roll(self,sigma_speed = 5, sigma_rotate = 0.01, dt = 1):
        """ ============================
            perform a step based on speed manipulation
            ============================ """
        # set new state
        self.v = min(max(self.v-1+self.gen.randn()*sigma_speed,0),
                         self.v_max) # 0<= speed <= v_max
        self.azimuth +=360*self.gen.randn()*sigma_rotate

        # print("Speed = {}, heading = {}".format(self.v, self.azimuth))
        # calculate new position based on the state
        self.calc_position(dt = dt)
        self.set_sensor_position()


    def random_step(self, sigma = 0.1):
        """ ============================
            perform a random rand_step
            ============================ """
        # loop until a valid move is found
        ii = 0
        while True:
            ii+=1
            # draw a step from the RNG (dx, xy)
            rand_step = self.gen.randn(1,2)[-1]

            # update the next position and check validity
            new_pos = Point(self.pos.vec+ rand_step*sigma)
            if (0<=new_pos.x<=self.limits.x) and (0<=new_pos.y<=self.limits.y):
                # we have a valid move -> update new position
                self.pos.vec = new_pos.vec
                self.set_sensor_position()
                return(new_pos)
            else:
                print('misstep {} at x = {}; y = {}'.format(ii,  new_pos.x, new_pos.y))

    def __str__(self):
        'print something useful'
        return "Ant {ID} at position ({x}, {y})".format(ID=self.ID, x=self.pos.x,y=self.pos.y)


def run():
    """ ==================
        Do something for testing
        ================== """
    D = Ant()
    # print(D.pos)
    # for i in range(10):
    #     D.random_roll(dt = 0.1)
    #     print("Speed = {}, heading = {} ; {}".format(D.v,D.azimuth, D))
    # D.set_sensor_position()
    print(D.observed_pheromone([3,-1],activation = 'linear'))
    D.gradient_step(Q=D.observed_pheromone([0,1]),theta_max=360)
    print(D)



if __name__ == '__main__':
    run()
