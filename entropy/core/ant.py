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

        " Properties "
        self.id = id
        self.pos = point(*start_pos) # in mm [x,y]
        self.azimuth = angle #azimuth angle in degrees (counterclockwise, base x-axis)
        self.limits = point(*limits)
        self.l = l # antenna length from CoM (mm)
        self.antenna_offset = antenna_offset #angle between centerline and antennas
        self.v = speed
        self.Qobserved = [0,0] #observed pheromone

        " Sensor specific properties "
        self.sensors = {} #initialize dictionary
        self.set_sensor_position()

        " States "
        self.foodbound = False
        self.out_of_bounds = False

    def set_sensor_position(self):
        """ calculate the sensor locations based on length, rotation and offset """
        self.sensors['left'] = point(*self.pos.vec+T_matrix(self.azimuth
                                      + self.antenna_offset).dot([self.l,0]))
        self.sensors['right'] = point(*self.pos.vec+T_matrix(self.azimuth
                                      - self.antenna_offset).dot([self.l,0]))

    @property
    def azimuth(self):
        return self._azimuth
    @azimuth.setter
    def azimuth(self, a):
        """ ensure azimuth in [0,360] """
        if a < 0: self._azimuth = 360+(a%-360)
        else: self._azimuth = a%360


    def observe_pheromone(self, fun, Q, fun_args = {}):
        """ pass Q into the observation function,
            return list of observed pheromone based on the absolute quantity
            in Q """
        self.Qobserved = [fun(q, **fun_args) for q in Q]

    def gradient_step(self, gain, dt = 1):
        """ update azimuth based on difference in observed pheromone
            Q[0] == 'left', Q[1]=='right', counterclockwise positive turn"""
        Q = self.Qobserved
        self.azimuth += gain*(Q[0]-Q[1]) #rotate
        self.step(dt) #step in new direction
        self.set_sensor_position() #update sensor location

    def step(self, dt):
        """ do a step in the current direction, do boundary checking as well """
        new_pos = point(*self.pos.vec+T_matrix(self.azimuth).dot([self.v*dt,0]))

        " Check limits "
        self.out_of_bounds = True # assume out of bounds
        if new_pos.x >= self.limits.x: new_pos.x = self.limits.x #upper limit x
        elif new_pos.y >= self.limits.y: new_pos.y = self.limits.y #upper limit y
        elif new_pos.x <= 0: new_pos.x = 0 #lower limit x
        elif new_pos.y <= 0: new_pos.y = 0 # lower limit y
        else: self.out_of_bounds = False #turns out, not out of bounds

        " Update position "
        self.pos = new_pos


ant_settings = {'start_pos': [10,10],
                'angle': 45,
                'speed': 10,
                'limits': [1000,1000],
                'l': 10,
                'antenna_offset': 30}

def lin_fun(x):
    return 10*x

def return_fun(fun,arg):
    return fun(arg)

def test_ant():
    ant = Ant(**ant_settings)
    print(return_fun(lin_fun,10))
    print(ant.sensors['left'].vec)
    print(ant.sensors['right'].vec)
    print(ant.observerd_pheromone(lin_fun,[1,1]))
    ant.gradient_step(1,1)
def time_it():
    "Time all the steps of the ant class, using time for timit bian a PIA"
    import time
    ant = Ant(**ant_settings)
    n = int(1e5)

    " Observe pheromone "
    tic = time.time()
    for Q in np.random.randn(n,2):
        ant.observe_pheromone(lin_fun,Q)
    toc = time.time()
    print("Observed pheromone in avg {} msec".format(1e3*(toc-tic)/n))

    " Step "
    tic = time.time()
    for _ in range(n):
        ant.step(1)
    toc = time.time()
    print("Stepped in avg {} msec".format(1e3*(toc-tic)/n))

    " Update sensors "
    tic = time.time()
    for _ in range(n):
        ant.set_sensor_position()
    toc = time.time()
    print("Updated sensors in avg {} msec".format(1e3*(toc-tic)/n))


    " Total gradient step "
    tic = time.time()
    for Q in np.random.randn(n,2):
        ant.observe_pheromone(lin_fun,Q)
        ant.gradient_step(1,1)
    toc = time.time()
    print("Total step took avg {} msec".format(1e3*(toc-tic)/n))

if __name__ == '__main__':
    time_it()
