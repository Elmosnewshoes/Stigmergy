import numpy as np
import time
from small_functions import T_matrix, Point
from collections import namedtuple

state = namedtuple('state', 'speed angle')

class Ant():
    """ ===========================
        The main agents/actors in the simulation
        =========================== """
    # start_pos (x,y) in mm
    # limits (x_lim, y_lim) in mm

    def __init__(self, start_pos = (1,1), limits = (10,10), ant_id =0, speed=0, angle=0, v_max = 0):
        """  =================================
            Initialize the class
            ================================== """
        # give the agent an ID (int)
        self.ID = ant_id

        # set the start coordinates and domain limits
        self.pos = Point(start_pos) #ant (starting) position in mm
        self.orientation = 0 # angle between ant and x-axis (Counter-Clockwise positive)
        self.limits = Point(limits)  #domain limits in mm

        # ant physical properties
        self.l = 3 #length in mm (distance between CoM and sensors)
        self.antenna_offset = 30 #angle (grad) between centerline and antenna from the base of the antenna
        self.sensors = {'left':Point([0,0]), #position of the sensors (absolute)
                   'right': Point([0,0])}


        # assign private RNG
        self.gen = np.random.RandomState()

        # set the physical state of the ant
        self.v_max = v_max
        self.state = state(speed, angle)

    def __str__(self):
        'print something useful'
        return "Ant {ID} at position ({x}, {y})".format(ID=self.ID, x=self.pos.x,y=self.pos.y)

    def set_sensor_position(self):
        """ ============================
            set the absolute location of the sensors based on the ants' properties
            and orientation/position
            ============================ """
        self.sensors['left'].vec = (self.pos.vec
                                    + np.dot(self.l,[1,0])
                                    *T_matrix(self.orientation
                                              + self.antenna_offset))
        self.sensors['right'].vec = (self.pos.vec
                                     + np.dot(self.l,[1,0])
                                     *T_matrix(-self.orientation
                                               - self.antenna_offset))


    def random_roll(self,sigma_speed = 0.1, sigma_rotate = 0.1):
        """ ============================
            perform a step based on speed manipulation
            ============================ """



    def random_step(self, sigma = 0.1):
        """ ============================
            perform a random rand_step
            ============================ """
        # loop until a valid move
        ii = 0
        while True:
            ii+=1
            # draw a step from the RNG (dx, xy)
            rand_step = self.gen.randn(1,2)[-1]

            # update the next position and check validity
            new_pos = Point(self.pos.vec+ rand_step*sigma)
            if (0<=new_pos.x<=self.limits.x) and (0<=new_pos.y<=self.limits.y):
                # we have a valid move -> update new position
                self.pos = new_pos
                return(new_pos)
            else:
                print('misstep {} at x = {}; y = {}'.format(ii,  new_pos.x, new_pos.y))


def run():
    """ ==================
        Do something for testing
        ================== """
    D = Ant()
    # print(D.pos)
    # print(D.random_step())
    D.set_sensor_position()
    print(D)


if __name__ == '__main__':
    run()
