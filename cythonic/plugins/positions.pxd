cdef struct point:
    double x
    double y

cdef struct index:
    unsigned long x
    unsigned long y

# cdef class point:
#     cdef public double[2] xy
#     cdef readonly double cx(self)
#     cdef readonly double cy(self)
#
# cdef class index:
#     # unsigned integer, grid location
#     cdef:
#         public unsigned long[2] xy
#         readonly unsigned long cx(self)
#         readonly unsigned long cy(self)

cdef struct map_range:
    unsigned long[3] x
    unsigned long[3] y
