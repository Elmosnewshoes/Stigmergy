cdef void dep_constant(double * x, ant_state* s, dep_fun_args* args):
    " constant, deposit quantity := q "
    " x == memory location to store"
    x[0]=  args[0].q
