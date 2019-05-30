# distutils: language = c++

from cythonic.plugins.functions cimport transform
from cythonic.plugins.sens_functions cimport observe_linear, observe_relu
from cythonic.plugins.dep_functions cimport dep_constant, dep_exdecay
from cythonic.plugins.rotate_functions cimport simple, weber, override
# from cythonic.plugins.drop_functions cimport exp_decay
# import numpy as np
from libc.math cimport M_PI as PI
# from cythonic.plugins.rng cimport RNG

cdef class Ant:
    def __cinit__(self, double l, double d, double sens_offset, double gain, str sens_fun,
        double noise_gain, double noise_gain2, dict sens_dict, str rotate_fun, double steer_regularization, override, **kwargs):
        " set global ant constants "
        self.l = l #antenna length/offset
        self.d = d #stinger offset
        self.sens_offset = sens_offset #degrees /angular offset
        # self.gain = gain
        # self.noise_gain = noise_gain # fraction of self.gain
        self.current_step = 0 #current step in simulation
        self.override = override
        self.override_max = kwargs['override_max']
        self.override_time = kwargs['override_time']


        " === Assign sensor activation function === "
        if sens_fun =='linear':
            self.sens_fun = observe_linear
        elif sens_fun == 'ReLu':
            self.sens_fun = observe_relu

        "=== Assign steering function (control algorithm) ==="
        if rotate_fun == 'simple':
            self.rotate_fun = simple
        elif rotate_fun == 'weber':
            self.rotate_fun = weber

        "=== Load the structs for sensing and steering ==="
        self.obs_fun_args = sens_dict
        self.rot_fun_args = {'covariance_1': noise_gain,
                                'covariance_2': noise_gain2,
                                'alpha': gain,
                                'k': steer_regularization}


    """ ================ Deposit related methods ================== """
    cdef void set_actuator_args(self, str fun, dep_fun_args args, ):
        " setup the actuator (pheromone deposit) specific parameters "
        self.dep_args = args
        if fun == 'constant':
            self.dep_fun = dep_constant
        elif fun == 'exp_decay':
            self.dep_fun = dep_exdecay

    cdef void calc_quantity(self,double * q):
        " fill the pheromone-dropped-quantity memory location "
        # q is the placeholder for the returned quantity
        # self.dep_fun(double * x, ant_state* s, dep_fun_args* x)
        # q == pointer to mem location of quantity
        # self.state == already pointer to ant_state
        if self.state[0].out_of_bounds:
            q[0] =0
        else:
            self.dep_fun(q, self.state, &self.dep_args )

    """ ================ observation related methods ================ """
    cdef void observe(self, observations* Q):
        " fill Q_obs(lft, right) based on sensing function "
        if self.state[0].out_of_bounds:
            #either left or right sensor senses 0!
            self.state[0].Q_obs.lft = Q[0].lft
            self.state[0].Q_obs.rght = Q[0].rght
        else:
            self.sens_fun(self.state, &self.obs_fun_args, Q)

    """ ================ step related methods ================ """
    cdef void next_step(self):
        "simply increase the counter"
        self.current_step+=1

    cdef void rotate(self,double* dt):
        " rotate the ant based on angular velocity omega "
        " compute the angular speed (degrees/second) based on sensing "
        self.rotate_fun(s = self.state, args = &self.rot_fun_args, cur_step = &self.current_step)
        if self.override and not self.state[0].foodbound:
            # ant is nestbound and gets a nudge in the right direction
            override(s = self.state, l = &self.l ,t_max = &self.override_time, override_max = &self.override_max, dt = dt)
        self.increase_azimuth(dt) # state is known, no need to pass it

    cdef void gradient_step(self, double *dt, observations * Q):
        " execute the sequence for differential based stepping "
        " sniff pheromone -> rotate -> step -> update sensors "
        self.observe(Q)
        self.rotate(dt)
        self.step(dt)
        self.state[0].time += dt[0] # update internal timer
        self.set_sensors()

    cdef void step(self, double * dt):
        " do a step in the current direction "

        " update position "
        cdef double step_size = self.state[0].v*dt[0]
        self.state[0].pos = transform(self.state[0].theta, &step_size, &self.state.pos)

    cdef void set_sensors(self):
        " calculate the position of the left and right sensor antennas "
        self.state[0].left = transform(self.state[0].theta + self.sens_offset, &self.l, &self.state.pos)
        self.state[0].right = transform(self.state[0].theta - self.sens_offset, &self.l, &self.state.pos)
        self.state[0].dropper = transform(self.state[0].theta + 180, &self.d, &self.state.pos)

    cdef void increase_azimuth(self, double * dt):
        " ensure azimuth stays within [0,360) interval "
        " increase azimuth based on the angular speed and the time interval "
        self.state[0].theta = (self.state[0].theta+self.state[0].omega*dt[0])%360

    cdef void reverse(self):
        " turn around "
        self.state[0].theta += 180
        self.set_sensors()

    """ ================ State sensing methods ================ """

    cdef void out_of_bounds(self, bint oob):
        " toggle out of bounds status "
        self.state[0].out_of_bounds = oob

    cdef readonly void foodbound(self):
        self.state[0].foodbound = True
        self.state[0].nest = self.state[0].pos

    cdef readonly void nestbound(self):
        self.state[0].foodbound = False

    cdef void activate(self):
        " mark the ant as active "
        self.state[0].active = True

    cdef void set_state(self,ant_state* s):
        " assign the ant a state "
        self.state = s
