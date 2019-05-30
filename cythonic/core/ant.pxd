# distutils: language = c++

from cythonic.plugins.positions cimport point
from cythonic.plugins.sens_structs cimport fun_args, observations
from cythonic.plugins.dep_structs cimport dep_fun_args
from cythonic.plugins.rotate_structs cimport  rotate_args
from libcpp.vector cimport vector

#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
ctypedef readonly void (*f_obs)(ant_state*,fun_args*, observations*) #type definition for sensing functions
ctypedef readonly void (*f_dep)(double * x, ant_state* s, dep_fun_args* args)
ctypedef readonly void (*f_rot)(ant_state* s, rotate_args* args, unsigned int * cur_step)

cdef struct ant_state:
    # " position and orientation "
    unsigned int id
    point pos #{x,y} in mm
    point dropper # deposit location
    point left #left sensor location
    point right #right sensor location
    double theta #azimuth in degrees
    double omega #angular rotation in degrees/second
    double v # mm/s
    point nest #location where ant left nest for the last time
    observations Q_obs
    vector[double] noise_vec_1 #pre-populate the observation noise
    vector[double] noise_vec_2

    #" ant status "
    bint foodbound
    bint active
    bint out_of_bounds

    #" individual timers "
    double time #time since last event


cdef class Ant:
    " attributes "
    cdef ant_state* state
    cdef:
        # " geometric properties "
        double l, d
        double sens_offset

        # sensor properties
        # double gain
        # double noise_gain
        rotate_args rot_fun_args
        f_rot rotate_fun
        f_obs sens_fun
        fun_args obs_fun_args
        unsigned int current_step

        # actuator properties
        f_dep dep_fun
        dep_fun_args dep_args

    " c-only methods (all readonly) "
    cdef:
        readonly void foodbound(self)
        readonly void nestbound(self)
        readonly void rotate(self,double* dt)
        readonly void gradient_step(self, double *dt, observations * Q)
        readonly void observe(self, observations* Q)
        readonly void step(self, double * dt)
        readonly void out_of_bounds(self, bint oob)
        readonly void set_sensors(self)
        readonly void set_actuator_args(self, str fun, dep_fun_args args, )
        readonly void calc_quantity(self,double * q)
        readonly void activate(self)
        readonly void increase_azimuth(self, double * dt)
        readonly void set_state(self,ant_state* s)
        readonly void reverse(self)
        readonly void next_step(self)
