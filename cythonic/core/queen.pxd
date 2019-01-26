# distutils: language = c++

# from cythonic.plugins.positions cimport ant_state
# cdef class queen():
#     " attributes "
#     cdef list ants
#     cdef unsigned int n
#     cdef unsigned int count_active
#
#     "CPython methods "
#     cpdef void deploy(self)
#     cpdef void reverse(self)
#     cpdef void gradient_step(self,double dt, str observe_fun, double[:] Q)
#     cpdef void observe_pheromone(self,str observe_fun, double[:] Q)
#     cdef readonly void activate(self, ant_state s)
from libcpp.vector cimport vector
from cythonic.plugins.sens_structs cimport  observations
from cythonic.plugins.positions cimport point
from cythonic.plugins.dep_structs cimport dep_fun_args

from cythonic.core.ant cimport Ant, ant_state
cdef class Queen:
    cdef public vector[ant_state] state_list
    cdef public vector[observations] pheromone_vec
    cdef readonly Ant agent #" ant template "
    cdef:
        readonly unsigned int n
        readonly unsigned int count_active
        readonly double dt
        readonly double default_speed
        readonly double[:] drop_quantity
    # methods
    cdef readonly void setup_ant_depositing(self,str fun_type, dep_fun_args args)
    cdef readonly void step(self, double * dt)
    cdef readonly ant_state generate_state(self, point p, double theta)
    cpdef readonly void initialize_states(self,double[::,:] xy, double[:] theta)
    cdef readonly void deploy(self, unsigned int ant_id)
    cdef readonly void step_all(self,)
    cdef readonly void assign_state(self,unsigned int *ant_id)
    cdef readonly void gradient_step(self, observations * Q)
    cpdef readonly void print_pos(self)
