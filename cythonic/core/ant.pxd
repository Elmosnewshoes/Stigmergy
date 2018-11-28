from cythonic.plugins.positions cimport point
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

        # drop quantity related
        readonly double[2] q_observed
        readonly double _drop_quantity, return_factor
        readonly double time, v, drop_beta
        readonly str drop_fun

        # sensing related
        readonly RNG rng

    " cpython methods "
    cpdef readonly void init_positions(self, double[:])
    cpdef public double return_drop_quantity(self)
    cpdef public void gradient_step(self,double)
    cdef void increase_azimuth(self, double *)

    " C-only methods "
    cdef public void step(self,double *)
    cdef public bint correct_bounds(self)
    cdef void set_sensors(self)
    cdef void observe(self,str , double[2])
    cdef void rotate(self, double *)
    # cpdef void step(self,double)
