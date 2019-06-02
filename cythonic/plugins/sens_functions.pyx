# distutils: language = c++
from libc.math cimport exp as cexp, fmax as cmax
import numpy as np

cdef double lin(double *x):
    return x[0]

# from cythonic.core.ant cimport ant_state
cdef void observe_linear(ant_state* s, fun_args* a, observations* Q):
    " linear observation: Q = (q)*gain with"
    s[0].Q_obs.lft = Q[0].lft
    s[0].Q_obs.rght = Q[0].rght

# from cythonic.core.ant cimport ant_state
cdef void observe_relu(ant_state* s, fun_args* a, observations* Q):
    " ReLu: Q = min(q,k)"
    s[0].Q_obs.lft = cmax(Q[0].lft,a[0].breakpoint)
    s[0].Q_obs.rght =cmax(Q[0].rght,a[0].breakpoint)

cdef void sigmoid(ant_state* s, fun_args* a, observations* Q):
    """ observation: """

cdef vector[double] telegraph_noise(unsigned int sz,double dt, double beta):
    " make a series of random values based on a telegraph random process "
    " s = sgn *0.5 + e -0.5 -> s between [-1,1] since random e from U[0,1]"
    cdef double time = 0., t_hop = 0.
    cdef vector[double] output
    cdef double sgn = <double> np.sign(np.random.randn()) # can have values -1, 1
    cdef double scale = 1/beta
    for i in range(sz):
        " populate output vector "
        if time >= t_hop:
            time = 0 # reset timer
            t_hop =np.random.exponential(scale)  # duration of validity of new sgn variable
            sgn  = -sgn  # flip
        time +=dt
        output.push_back(sgn*0.5+np.random.randn()) #
    return output
