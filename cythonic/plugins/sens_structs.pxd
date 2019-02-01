cdef struct fun_args:
    double breakpoint
    # double snr # as in, fraction of noise_gain w.r.t. steering gain
    double exp_lambda # parameter for exponential distribution pdf: f(x,l) = l*exp(-l*x)
    # cdf exp distribution: F(x,l) = 1-exp(-l*x) for x>= 0

cdef struct observations:
    double lft
    double rght
