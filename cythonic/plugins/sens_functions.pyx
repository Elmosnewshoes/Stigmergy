# distutils: language = c++
from libc.math cimport exp as cexp
import numpy as np

cdef double lin(double *x):
    return x[0]

# from cythonic.core.ant cimport ant_state
cdef void observe_linear(ant_state* s, fun_args* a, observations* Q):
    " linear observation: Q = (q+epsion)*gain with espilon random number"
    s[0].Q_obs.lft = Q[0].lft
    s[0].Q_obs.rght = Q[0].rght

cdef void sigmoid(ant_state* s, fun_args* a, observations* Q):
    """ observation: """

cdef vector[double] telegraph_noise(unsigned int sz,double dt, double beta):
    " make a series of random values based on a telegraph random process "
    " s = sgn *0.5 + e -0.5 -> s between [-1,1] since random e from U[0,1]"
    cdef double time = 0., t_hop = 0.
    cdef vector[double] output
    cdef double sgn # can have values -1, 0 or 1
    for i in range(sz):
        " populate output vector "
        if time >= t_hop:
            time = 0 # reset timer
            t_hop =1-np.exp(-beta*np.random.rand())  # duration of validity of new sgn variable
            sgn  = <double> np.sign(np.random.randn())  # draw random sign variable
        time +=dt
        output.push_back(sgn*0.5+np.random.rand()-.5) # output bounded between [-1,1] with mean zero
    return output
