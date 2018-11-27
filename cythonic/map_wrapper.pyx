from cythonic.core.map cimport  GaussMap,MeshMap
from cythonic.plugins.positions cimport point, index, map_range

import numpy as np
X = np.array([1,2,3], dtype = np.float64)
Y = np.array([4,100,11], dtype = np.float64)
cdef map_range I
I.x = X
I.y = Y
cpdef void print_I():
    print(I)


cdef class MMap(MeshMap):
    " inherit the meshmap and publish its methods to python "
    def attributes(self):
        return [attr for attr in dir(self)
                  if not attr.startswith('__') and not attr == 'attributes']

    def get_bounds(self,vec,R):
        cdef point p = point(vec[0],vec[1])
        cdef double r = R
        cdef index i = index(self.to_grid(&p.x),self.to_grid(&p.y))
        return self.span(&i.x,&i.y,&r)
