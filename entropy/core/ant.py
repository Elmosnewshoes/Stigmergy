""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """
import numpy as np
from plugins.helper_functions import T_matrix
from plugins.helper_classes import point, loc

class Ant:
    """ Class for the agent/actor in the sim"""
    def __init__(self, start_pos, angle, speed, limits, l, antenna_offset):
        """ all dimensions in mm """

        # set properties
        self.id = id
        self.pos = point(*start_pos) # in mm [x,y]
        self.azimuth = angle #azimuth angle in degrees (counterclockwise, base x-axis)
        self.limits = point(*limits)
        self.l = l # antenna length from CoM (mm)
        self.antenna_offset = antenna_offset #angle between centerline and antennas
        self.v = speed

        self.sensors = {} #initialize dictionary
        self.set_sensor_position()

    def set_sensor_position(self):
        self.sensors['left'] = (self.pos.vec
                                + np.dot(self.l,[1,0])
                                *T_matrix(self.azimuth
                                      + self.antenna_offset).transpose())
        self.sensors['right'] = (self.pos.vec
                                 + np.dot(self.l,[1,0])
                                 * T_matrix(self.azimuth
                                        - self.antenna_offset).transpose())

    @property
    def azimuth(self):
        return self._azimuth
    @azimuth.setter
    def azimuth(self, a):
        """ ensure azimuth in [0,360] """
        if a < 0: self._azimuth = 360+(a%-360)
        else: self._azimuth = a%360


def lin_fun(x):
    return 10*x

def return_fun(fun,arg):
    return fun(arg)

def test_ant():
    ant_settings = {'start_pos': [10,10],
                    'angle': 360*np.random.rand(),
                    'speed': 10,
                    'limits': [1000,1000],
                    'l': 10,
                    'antenna_offset': 30}
    ant = Ant(**ant_settings)
    print(ant.azimuth)
    print(return_fun(lin_fun,10))
if __name__ == '__main__':
    test_ant()
