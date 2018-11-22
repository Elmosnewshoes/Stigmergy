cimport numpy as np
import numpy as np
from cythonic.plugins.positions cimport point, index
from libc.math cimport lrint # round double, cast as long

cdef class MeshMap:
    def __cinit__(self, double[:] dim, double resolution):
        """ base class for a meshgrid and some supporting functions """
        " assume dim is vector[2]=> [double x, double y]"
        self.dim = point(dim[0], dim[1])
        self.pitch = resolution
        self.lim = index(self.to_grid(&self.dim.xy[0]),self.to_grid(&self.dim.xy[1]))
        self.map = np.ones((self.lim.x+1,self.lim.y+1),dtype = np.float_)

    cdef readonly unsigned long to_grid(self, double * x):
        " round point in mm to grid index "
        return lrint(x[0]/self.pitch)

    cdef readonly double to_mm(self,unsigned long * x):
        " convert grid index to location in mm "
        return <double>self.pitch*x[0]
