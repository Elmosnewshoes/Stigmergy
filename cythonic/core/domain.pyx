from cythonic.plugins.positions cimport point, index, map_range
from cythonic.core.map cimport MeshMap, GaussMap
cimport numpy as np
import numpy as np
from libc.math cimport ceil as cceil, sqrt as csqrt, log as cln
cimport cython

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
cdef class domain:
    " playground of the simulation "

    cdef readonly void init_gaussian(self, double sigma, double significancy):
        " initialize a gaussian meshmap "
        cdef double R = cceil(sigma*csqrt(2*cln(significancy)))
        self.Gaussian = GaussMap(resolution = self.Map.pitch, R = R, covariance = sigma)

    cdef bint check_bounds(self, double* x, double* y):
        " check if point is within the domain limits"
        if x[0] >=0 and y[0]>=0 and \
            x[0]<=self.size.x and y[0]<= self.size.y:
            return True
        else:
            return False

    cdef readonly double probe_pheromone(self,point * p):
        " return the pheromone quantity at a location on the map "
        cdef double Q
        if self.check_bounds(&p.x, &p.y):
            " convert point to index "
            Q = self.Map.map[self.Map.to_grid(&p.y),self.Map.to_grid(&p.x)]
        else:
            " out of bounds, return zero "
            Q = 0.
        return Q

#     cdef readonly void add_pheromone(self,double[:,::1] mp, double[:,::1] gauss, point *p, double *Q):
    cdef readonly void add_pheromone(self,point *p, double *Q):
        " add quantity Q pheromone at gaussian centered around p "
        cdef index I = index(self.Map.to_grid(&p.x),self.Map.to_grid(&p.y))
        cdef map_range s = self.Map.span(&I.x,&I.y,&self.Gaussian.radius)
        cdef long offset_x = self.Map.to_grid(&p.x)-s.x[1]+s.x[0]
        cdef long offset_y = self.Map.to_grid(&p.y)-s.y[1]+s.y[0]
        cdef long i,j
        for i in range(s.y[2]-s.y[0]):
            for j in range(s.x[2]-s.x[0]):
                self.Map.map[offset_y+i,offset_x+j]+=Q[0]*self.Gaussian.map[i+s.y[0], j+s.x[0]]
#                 mp[offset_y+i,offset_x+j]+=Q[0]*gauss[i+s.y[0], j+s.x[0]]


    def __cinit__(self,size,pitch,nest_loc, nest_rad, food_loc, food_rad):
        self.size = point(size[0],size[1])
        self.nest_location = point(nest_loc[0],nest_loc[1])
        self.food_location = point(food_loc[0],food_loc[1])
        self.nest_radius = nest_rad
        self.food_radius = food_rad

        self.Map = MeshMap(dim = np.array(size, dtype = np.float_), resolution = pitch)
        self.dim = index(self.Map.map.shape[0],self.Map.map.shape[1])
