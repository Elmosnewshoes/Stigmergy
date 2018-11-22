cdef class point:
    cdef public double[2] xy
    cdef public double cx(self)
    cdef public double cy(self)

cdef struct location:
    # unsigned integer, grid location
    unsigned int x,y
