from cythonic.plugins.positions cimport point, index
from cythonic.core.map cimport MeshMap, GaussMap
from cythonic.plugins.sens_structs cimport observations
cdef class Domain:
    " attributes "
    cdef:
        readonly point size, nest_location, food_location
        readonly double pitch, nest_radius, food_radius
        readonly MeshMap Map
        readonly GaussMap Gaussian
        readonly index dim
        public double target_pheromone

    " methods"
    cdef:
        readonly void init_gaussian(self,double sigma, double significancy)
        readonly void fill_observations(self, observations * O, point * pos_left, point * pos_right)
        bint check_bounds(self, double*,double*)
        readonly double probe_pheromone(self,point*)
        readonly void add_pheromone(self,point *p, double *Q)
        readonly void pyvaporate(self)
        readonly void cvaporate(self)
        readonly void set_target_pheromone(self,double target)
