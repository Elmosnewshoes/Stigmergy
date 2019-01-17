from cythonic.plugins.functions cimport transform
from cythonic.plugins.sens_functions cimport observe_linear
# from cythonic.plugins.drop_functions cimport exp_decay
# import numpy as np
from libc.math cimport M_PI as PI
# from cythonic.plugins.rng cimport RNG

cdef class Ant:
    def __cinit__(self, double l, double sens_offset, double gain, double drop_quantity, double return_factor,
                 double drop_beta):
        self.l = l
        self.sens_offset = sens_offset
        self.gain = gain
        self.drop_quantity = drop_quantity
        self.return_factor = return_factor
        self.drop_beta = drop_beta
        self.sens_fun = observe_linear
        self.obs_fun_args.gain = 1

    cdef void rotate(self,double* dt):
        " compute the angular speed (degrees/second) based on sensing "
        self.state[0].omega = self.gain*180./PI*(
            self.state[0].Q_obs.lft-self.state[0].Q_obs.rght)
        self.increase_azimuth(dt)

    cdef void gradient_step(self, double *dt, observations Q):
        " execute the sequence for differential based stepping "
        " sniff pheromone -> rotate -> step -> update sensors "

        self.observe(&Q)
        self.rotate(dt)
        self.step(dt)
        self.set_sensors()

    cdef void observe(self, observations* Q):
        # fill Q_obs(lft, right)
        self.sens_fun(self.state, &self.obs_fun_args, Q)

    cdef void step(self, double * dt):
        " do a step in the current direction ,do boundary check as well "
        self.state[0].time += dt[0] # update internal timer

        # update position
        cdef double step_size = self.state[0].v*dt[0]
        self.state[0].pos = transform(self.state[0].theta, &step_size, &self.state.pos)

    cdef void out_of_bounds(self, bint oob):
        " toggle out of bounds status "
        self.state[0].out_of_bounds = oob

    cdef void set_sensors(self):
        " calculate the position of the left and right sensor antennas "
        self.state[0].left = transform(self.state[0].theta + self.sens_offset, &self.l, &self.state.pos)
        self.state[0].right = transform(self.state[0].theta - self.sens_offset, &self.l, &self.state.pos)

    cdef void activate(self):
        " mark the ant as active "
        self.state[0].active = True

    cdef void increase_azimuth(self, double * dt):
        " ensure azimuth stays within [0,360) interval "
        " increase azimuth based on the angular speed and the time interval "
        self.state[0].theta = (self.state[0].theta+self.state[0].omega*dt[0])%360

    cdef void set_state(self,ant_state* s):
        self.state = s
