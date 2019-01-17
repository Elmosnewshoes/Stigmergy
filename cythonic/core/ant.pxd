from cythonic.plugins.positions cimport point, ant_state
from cythonic.plugins.rng cimport RNG

#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION


cdef class Ant:
    " attributes "
    cdef:
        #physical properties
        readonly double l
        readonly unsigned int id
        readonly point limits

        # environment interaction
        readonly double gain,sens_offset

        #states
        readonly bint foodbound, out_of_bounds
        readonly double _azimuth
        readonly point _pos, _left, _right
        readonly bint active
        readonly double v
        readonly double time #time since last visit of nest/food
        readonly double rng_time #timer for the rng

        # drop quantity related
        readonly double[2] q_observed
        readonly double _drop_quantity, return_factor,  drop_beta
        readonly str drop_fun

        # sensing related
        readonly RNG rng

    " CPython methods "
    cpdef public void gradient_step(self,double dt, str observe_fun, double[:] Q)

    " C-only methods "
    # cdef readonly void init_state(self,ant_state * x)
    cdef readonly void step(self,double * dt)
    cdef readonly void activate(self, ant_state s)
    # cdef readonly void init_positions(self, double[:])
    cdef public double return_drop_quantity(self, double *dt)
    cdef void increase_azimuth(self, double *)
    cdef public bint correct_bounds(self)
    cdef void set_sensors(self)
    cdef void observe(self,str observe_fun, double[:] Q)
    cdef void rotate(self, double * dt)
    # cpdef void step(self,double)
