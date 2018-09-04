import numpy as np
import time
from collections import namedtuple

xy = namedtuple('coordinates', 'x y')
state = namedtuple('state', 'speed angle')

class Ant():
    """ ===========================
        The main agents/actors in the simulation
        =========================== """
    # start_pos (x,y) in mm
    # limits (x_lim, y_lim) in mm

    def __init__(self, start_pos = (1,1), limits = (10,10), ant_id =0, speed=0, angle=0):
        """  =================================
            Initialize the class
            ================================== """
        # give the agent an ID (int)
        self.id = ant_id

        # set the start coordinates and domain limits
        self.pos = xy._make(start_pos) #ant (starting) position in mm
        self.limits = xy._make(limits)  #domain limits in mm

        # ant physical properties
        self.l = 3 #length in mm
        self.antena_offset = 30*np.pi/(180) #angle (rad) between centerline and antenna from the base of the antenna

        # assign private RNG
        self.gen = np.random.RandomState()

        # set the physical state of the ant
        self.state = state(speed, angle)

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
            # draw a step from the RNG
            rand_step = self.gen.randn(2,1)

            # update the next position and check validity
            pos = [[self.x],[self.y]] + rand_step*sigma
            if (0<=pos[0][0]<=self.limits[0]) and (0<=pos[1][0]<=self.limits[1]):
                # we have a valid move -> update new position
                self.x = pos[0][0]
                self.y = pos[1][0]
                return((self.x,self.y))
            else:
                print('misstep {} at x = {}; y = {}'.format(ii,  pos[0][0], pos[1][0]))


    # def

def run():
    """ ==================
        Do something for testing
        ================== """
    D = Ant()
    print(D.pos)
    # D.random_step()
    # print(D.x,D.y)

if __name__ == '__main__':
    run()
