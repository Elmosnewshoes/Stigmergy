cdef class point:
    cdef public double[2] xy
    cdef public double cx(self)
    cdef public double cy(self)

cdef struct location:
    # unsigned integer, grid location
    unsigned int x,y

# cdef double[:] pp_vec(point p):
#     cdef double[2] return_vec
#     return_vec[0] = p.x
#     return_vec[1 ]= p.y
#     return return_vec
