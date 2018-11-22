from libc.math cimport exp
cdef double exp_decay(double *q, double *t, double *beta):
    " multiplier q, time t[s] and exponential constant beta[-] "
    # return q*e^(-beta*t)
    return q[0]*exp(-beta[0]*t[0])
