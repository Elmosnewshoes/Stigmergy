cdef double lin(double *x):
    return x[0]

# from cythonic.core.ant cimport ant_state
cdef void observe_linear(ant_state* s, fun_args* a, observations* Q):
    s[0].Q_obs.lft = Q[0].lft*a[0].gain
    s[0].Q_obs.rght = Q[0].rght*a[0].gain
