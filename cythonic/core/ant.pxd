from cythonic.plugins.positions cimport point
from cythonic.plugins.sens_structs cimport fun_args, observations
from cythonic.plugins.dep_structs cimport dep_fun_args

#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
ctypedef readonly void (*f_obs)(ant_state*,fun_args*, observations*) #type definition for sensing functions
ctypedef readonly void (*f_dep)(double * x, ant_state* s, dep_fun_args* args)

cdef struct ant_state:
    # " position and orientation "
    unsigned int id
    point pos #{x,y} in mm
    point left #left sensor location
    point right #right sensor location
    double theta #azimuth in degrees
    double omega #angular rotation in degrees/second
    double v # mm/s
    observations Q_obs

    #" ant status "
    bint foodbound
    bint active
    bint out_of_bounds

    #" individual timers "
    double rng_timer # for the random number generator
    double time #time since last event


cdef class Ant:
    " attributes "
    cdef ant_state* state
    cdef:
        # " geometric properties "
        double l
        double sens_offset

        # sensor properties
        double gain
        f_obs sens_fun
        fun_args obs_fun_args

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
        readonly void set_actuator_args(self, str fun, dep_fun_args x, )
        readonly void calc_quantity(self,double * q)
        readonly void activate(self)
        readonly void increase_azimuth(self, double * dt)
        readonly void set_state(self,ant_state* s)
        readonly void reverse(self)
