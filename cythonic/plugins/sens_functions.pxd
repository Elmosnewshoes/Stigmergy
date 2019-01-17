from cythonic.plugins.sens_structs cimport fun_args, observations
from cythonic.core.ant cimport ant_state

cdef double lin(double *x)
# function type for observe function
# ctypedef readonly void (*f_obs)(ant_state*,fun_args*, observations*) #type definition for sensing functions

#sensing functions themselves
cdef void observe_linear(ant_state* s, fun_args* a, observations* Q)
