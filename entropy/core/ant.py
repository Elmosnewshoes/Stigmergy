""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """
import numpy as np
from core.plugins.helper_functions import T_matrix, lin_fun
from core.plugins.helper_classes import point, loc

class Queen:
    def __init__(self):
        """ Class for handling multiple ants as if it was a single """
        """ ant_kwargs contains constants like: l, antenna_offset,
            limits, speed"""
        self.n = 0 # placeholder for ant count
        self.ants = []

    @property
    def left(self):
        return [ant.sensors['left'] for ant in self.ants]

    @property
    def right(self):
        return [ant.sensors['right'] for ant in self.ants]

    def deploy(self, pos, angle, ant_kwargs):
        """ deploy n new ants """
        n = angle.size
        for i in range(n):
            "deploy the ant and store positions"
            with Ant(start_pos = pos[i],angle = angle[i],
                                 id = i+self.n,**ant_kwargs) as ant:
                self.ants.append(ant)
        "update ant count"
        self.n+=n

    def reverse(self):
        for ant in self.ants:
            ant.reverse()

    def gradient_step(self,dt):
        "Gradient step wrapper"
        for ant in self.ants:
            ant.gradient_step(dt)

    def observe_pheromone(self,fun, Q, fun_args = {}):
        "observe pheromone wrapper"
        # print(Q)
        for i in range(self.n):
            self.ants[i].observe_pheromone(fun,Q[i],fun_args)

class RNG(np.random.RandomState):
    def __init__(self,beta = 1):
        " inherrit the numpy random number generator "
        super().__init__()
        self.t = 0 #countdown timer
        self.beta = beta
        self.sign = 1

    def add_t(self,dt):
        self.t-=dt

    def exp_signed_rand(self):
        if self.t <=0:
            self.sign = self.rand()-0.5 # 1 or -1 (exceptionally rare: 0)
            self.t = self.exponential(self.beta)
        return self.sign*self.rand()




class Ant:
    """ Class for the agent/actor in the sim"""
    def __init__(self, start_pos, angle, speed, limits, l, antenna_offset,drop_quantity,
                 noise_gain,gain,id=0,beta=1):
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
        self.drop_quantity = drop_quantity # amount of pheromone to drop
        self.gain = gain

        """ Get the ant its own RNG and timer """
        self.rng = RNG(beta=beta)
        self.time = 0
        self.noise_gain = noise_gain
        
        " Sensor specific properties "
        self.sensors = {} #initialize dictionary
        self.set_sensor_position()

        " States "
        self.foodbound = True
        self.out_of_bounds = False

    def compute_noise(self,type):
        " compute noise value "
        # if type=='':


    def reverse(self,change_objective = True):
        " Turn around 180 degrees "
        self.azimuth += 180
        if self.foodbound and change_objective:
            self.foodbound = not self.foodbound
            target = 'food'
            print(f"Start looking for {target}")
        elif change_objective:
            self.foodbound = not self.foodbound
            target = 'nest'
            print(f"Start looking for {target}")

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
        """ ensure azimuth in [0,360] (more or less) """
        if a < 0: self._azimuth = 360+(a%-360)
        else: self._azimuth = a%360

    def observe_pheromone(self,fun, Q, fun_args = {}):
        """ pass Q into the observation function,
            return list of observed pheromone based on the absolute quantity
            in Q """
        self.Qobserved = [fun(q, **fun_args) for q in Q]

    def gradient_step(self, dt = 1):
        """ update azimuth based on difference in observed pheromone
            Q[0] == 'left', Q[1]=='right', counterclockwise positive turn"""
        Q = self.Qobserved
        self.azimuth += (self.gain*dt*180/np.pi*(Q[0]-Q[1]) #rotate
                         +self.gain*self.noise_gain*self.rng.exp_signed_rand()) #noise component
        self.step(dt) #step in new direction
        self.set_sensor_position() #update sensor location

    def step(self, dt):
        """ do a step in the current direction, do boundary checking as well """
        self.rng.add_t(dt) #update timer of the RNG
        new_pos = point(*self.pos.vec+T_matrix(self.azimuth).dot([self.v*dt,0]))

        " Check limits "
        xbound = True # assume out of bounds
        ybound = True
        if new_pos.x >= self.limits.x: new_pos.x = self.limits.x #upper limit x
        elif new_pos.x <= 0: new_pos.x = 0 #lower limit x
        else: xbound = False
        if new_pos.y >= self.limits.y: new_pos.y = self.limits.y #upper limit y
        elif new_pos.y <= 0: new_pos.y = 0 # lower limit y
        else: ybound = False #turns out, not out of bounds
        if xbound or ybound: self.out_of_bounds = True
        else:  self.out_of_bounds = False
        " Update position "
        self.pos = new_pos
        self.set_sensor_position()

    def __enter__(self):
        """ return when class is casted in 'with Ant as ..:"""
        return self
    def __exit__(self, type, value, traceback):
        """ Accompanies __enter__"""
        pass
