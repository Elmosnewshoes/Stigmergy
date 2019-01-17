cdef struct point:
    double x
    double y

cdef struct index:
    unsigned long x
    unsigned long y

# cdef struct full_state:
#     bint foodbound # flag for foodbound (alternative nestbound)
#     bint out_of_bounds # flag for being out of bounds
#     bint active # flag for being active in the simulation
#     double _azimuth # theta [degrees]
#     double v # ant speed [mm/s]
#     point _pos # ant position [x,y] in [mm]
#     double rng_time #timer for the random number generator
#     double time # timer for state based drop quantity


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
