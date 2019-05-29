# distutils: language = c++

from cythonic.plugins.sens_structs cimport fun_args, observations
from libcpp.vector cimport vector
from cythonic.core.ant cimport ant_state

cdef double lin(double *x)
# function type for observe function
# ctypedef readonly void (*f_obs)(ant_state*,fun_args*, observations*) #type definition for sensing functions

#sensing functions themselves of type void (*f_obs)
cdef void observe_relu(ant_state* s, fun_args* a, observations* Q)
cdef void observe_linear(ant_state* s, fun_args* a, observations* Q)
cdef void sigmoid(ant_state* s, fun_args* a, observations* Q)

# function for pre-calculating the observation noise
cdef vector[double] telegraph_noise(unsigned int sz,double dt, double beta)
