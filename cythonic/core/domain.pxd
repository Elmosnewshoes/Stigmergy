from cythonic.plugins.positions cimport point, index
from cythonic.core.map cimport MeshMap, GaussMap
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
        bint check_bounds(self, double*,double*)
        readonly double probe_pheromone(self,point*)
        readonly void add_pheromone(self,point *p, double *Q)
        readonly void pyvaporate(self)
        readonly void cvaporate(self)
        readonly void set_target_pheromone(self,double target)
