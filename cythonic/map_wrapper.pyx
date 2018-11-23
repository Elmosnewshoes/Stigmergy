from cythonic.core.map cimport  GaussMap
from cythonic.plugins.positions cimport point, index, map_range

import numpy as np
X = np.array([1,2,3], dtype = np.float64)
Y = np.array([4,100,11], dtype = np.float64)
cdef map_range I
I.x = X
I.y = Y
cpdef void print_I():
    print(I)


cdef class MMap(GaussMap):
    " inherit the meshmap and publish its methods to python "
    def attributes(self):
        return [attr for attr in dir(self)
                  if not attr.startswith('__') and not attr == 'attributes']
    def rounded(self, double x):
        return self.to_grid(&x)

    def get_bounds(self,loc,R):
        cdef double r = R
        return self.span(np.array(loc,dtype = np.uint64),&r)

    @property
    def vol(self):
        return self.volume
    @property
    def pk(self):
        return self.peak

    # def __cinit__(self,dim, resolution):
    #     super().__init__(dim,resolution)
