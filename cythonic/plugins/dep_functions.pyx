from libc.math cimport exp as cexp
cdef void dep_constant(double * x, ant_state* s, dep_fun_args* args):
    " constant, deposit quantity := q "
    " x == memory location to store"
    x[0]=  args[0].q

cdef void dep_exdecay(double * x, ant_state* s, dep_fun_args* args):
    " let the amount deposited decay with timer s.time "
    " exponential decay: dQ/dt=-lambda*Q -> Q(t) = Q(0)*exp(-lambda*t)"
    " halflife time == 1/lambda*ln(2) "
    " x== memory location to store the quantity "
    x[0] = args[0].q*cexp(-beta*s[0].time)
