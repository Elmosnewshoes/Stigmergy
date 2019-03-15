from cythonic.plugins.positions cimport point, index, map_range
from cythonic.core.map cimport MeshMap, GaussMap
cimport numpy as np
import numpy as np
from libc.math cimport ceil as cceil, sqrt as csqrt, log as cln
cimport cython
from cython.parallel cimport prange

cdef class Domain:
    " playground of the simulation "

    cdef readonly void fill_observations(self, observations * O, point * pos_left, point * pos_right):
        " do a  probe phermone on left and right point, store results in relayed observations struct "
        O[0].lft = self.probe_pheromone(pos_left)
        O[0].rght = self.probe_pheromone(pos_right)


    cdef readonly void init_gaussian(self, double sigma, double significancy):
        " initialize a gaussian meshmap "
        cdef double R = cceil(sigma*csqrt(2*cln(significancy)))
        self.Gaussian = GaussMap(resolution = self.Map.pitch, R = R, covariance = sigma)

    cdef readonly bint check_bounds(self, point * p):
        " check if point is within the domain limits"
        if p[0].x >=0 and p[0].y>=0 and \
            p[0].x<=self.size.x and p[0].y<= self.size.y:
            return True
        else:
            return False

    cdef readonly void constraint(self, point *p):
        " correct points outside the domain to be on the domain limit "
        if p[0].x <0:
            p[0].x = 0
        if p[0].x > self.size.x:
            p[0].x = self.size.x
        if p[0].y <0:
            p[0].y = 0
        if p[0].y > self.size.y:
            p[0].y = self.size.y

    cdef readonly bint check_pos(self, point * p, bint * foodbound):
        " check wheter point is at nest(nest==True)/food(nest==False)"
        if not foodbound[0]: #e.g. nestbound
            if (p[0].x-self.nest_location.x)**2+(p[0].y-self.nest_location.y)**2<= self.nest_radius**2:
                return True
            else:
                return False
        else: # e.g. foodbound
            if (p[0].x-self.food_location.x)**2+(p[0].y-self.food_location.y)**2<= self.food_radius**2:
                return True
            else:
                return False

    cdef readonly double probe_pheromone(self,point * p):
        " return the pheromone quantity at a location on the map "
        cdef double Q
        if self.check_bounds(p):
            " convert point to index "
            Q = self.Map.map[self.Map.to_grid(&p.y),self.Map.to_grid(&p.x)]
        else:
            " out of bounds, return zero "
            Q = 0.
        return Q

    cdef readonly void set_target_pheromone(self, double target):
        self.target_pheromone= target


    cdef void evaporate(self, double * tau):
        " evaporate, with rate tau "
        " if tau < 0 (typically -1 is used), use constant pheromone method "
        if tau[0] < 0.0:
            " call constant pheromone method "
            self.cvaporate()
            return
        " that return acts as if - else:"
        " do X[k+1] = tau * X[k]"
        cdef unsigned int i,j
        cdef unsigned int I = self.Map.map.shape[0]
        cdef unsigned int J = self.Map.map.shape[1]
        # for i in prange(I, nogil=True,schedule='static', chunksize=10):
        for i in range(I):
            for j in range(J):
                self.Map.map[i,j] *= tau[0]


    cdef readonly void cvaporate(self):
        " hard coded version of pyvaporate, roughly 7-12 times faster "
        " parallel computed sum of map yields another 2-3x speed boost "
        cdef double x = self.target_pheromone/self.Map.sum()
        cdef unsigned int i,j,I,J
        I = self.Map.map.shape[0]
        J = self.Map.map.shape[1]
        # print(f"Evaporation rate = {x}")
        for i in range(I):
            for j in range(J):
                self.Map.map[i,j] *=x
                # if self.Map.map[i,j] < 0.:
                #     raise ValueError('Map element smaller than 0')

    cdef readonly double entropy(self):
        " wraps Map.entropy method for easy coding "
        return self.Map.entropy()

    cdef readonly void pyvaporate(self):
        " evaporate the python way with constant volume"
        self.Map.map = np.dot(self.Map.map,self.target_pheromone/np.array(self.Map.map).sum())

    cdef readonly void add_pheromone(self,point *p, double *Q):
        " add quantity Q pheromone at gaussian centered around p "
        cdef index I = index(self.Map.to_grid(&p.x),self.Map.to_grid(&p.y))
        cdef map_range s = self.Map.span(&I.x,&I.y,&self.Gaussian.radius)
        cdef long offset_x = self.Map.to_grid(&p.x)-s.x[1]+s.x[0]
        cdef long offset_y = self.Map.to_grid(&p.y)-s.y[1]+s.y[0]
        cdef long i,j
        cdef double startsum = self.Map.sum()
        for i in range(s.y[2]-s.y[0]):
            for j in range(s.x[2]-s.x[0]):
                # print(f"Map[{offset_y+i}, {offset_x+j}] of [{self.Map.lim.x}, {self.Map.lim.y}]; Gaussian: [{i+s.y[0]}, {j+s.x[0]}] of [{self.Gaussian.lim.x}, {self.Gaussian.lim.y}]")
                # print(f"Adding {Q[0]*self.Gaussian.map[i+s.y[0], j+s.x[0]]}")
                # print(f"Target location: [{I.x}, {I.y}]")
                self.Map.map[offset_y+i,offset_x+j]+=Q[0]*self.Gaussian.map[i+s.y[0], j+s.x[0]]
#                 mp[offset_y+i,offset_x+j]+=Q[0]*gauss[i+s.y[0], j+s.x[0]]
        # print(f"Added {self.Map.sum()-startsum}: Q== {Q[0]}")

    cdef void reset(self):
        " reset the map "
        self.Map = MeshMap(dim=np.asarray([self.size.x,self.size.y], dtype = np.float_), resolution = self.Map.pitch)

    def __cinit__(self,size,pitch,nest_loc, nest_rad, food_loc, food_rad, target_pheromone = 1., **kwargs):
        self.size = point(size[0],size[1])
        self.nest_location = point(nest_loc[0],nest_loc[1])
        self.food_location = point(food_loc[0],food_loc[1])
        self.nest_radius = nest_rad
        self.food_radius = food_rad

        self.Map = MeshMap(dim = np.array(size, dtype = np.float_), resolution = pitch)
        self.dim = index(self.Map.map.shape[0],self.Map.map.shape[1])
        self.target_pheromone = target_pheromone * <double>self.dim.x*<double>self.dim.y
