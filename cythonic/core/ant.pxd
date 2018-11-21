from cythonic.plugins.positions cimport point
cpdef float cube(float)
#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION


cdef class Ant:
    " attributes "
    cdef:
        readonly double l
        readonly unsigned int id
        readonly double gain, v
        readonly bint foodbound, out_of_bounds
        readonly double _azimuth, sens_offset
        readonly point _pos, _left, _right
        readonly point limits

    " cp methods "
    cpdef readonly void init_positions(self, double[:])
    cpdef public void step(self,double)

    " C-only methods "
    cdef public bint correct_bounds(self)
    cdef void set_sensors(self)
    # cpdef void step(self,double)
