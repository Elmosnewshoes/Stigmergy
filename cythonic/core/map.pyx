cimport numpy as np
import numpy as np
from cythonic.plugins.positions import point

cdef class MeshMap:
    def __cinit__(self, dim, double resolution):
        """ base class for a meshgrid and some supporting functions """
        " assume dim is vector[2]=> [double x, double y]"
        self.dim = point(dim[0], dim[1])
