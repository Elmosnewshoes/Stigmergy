# distutils: language = c++
from cythonic.plugins.rotate_structs cimport rotate_args
from cythonic.core.ant cimport ant_state


cdef void simple(ant_state* s, rotate_args* args, unsigned int * cur_step)

cdef void weber(ant_state* s, rotate_args* args, unsigned int * cur_step)
# cdef double lin(double *x)
# function type for observe function
# ctypedef readonly void (*f_obs)(ant_state*,fun_args*, observations*) #type definition for sensing functions

#sensing functions themselves of type void (*f_obs)
# cdef void observe_linear(ant_state* s, fun_args* a, observations* Q)
# cdef void sigmoid(ant_state* s, fun_args* a, observations* Q)
