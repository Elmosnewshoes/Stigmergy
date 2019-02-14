from cythonic.core.ant cimport ant_state
from cythonic.plugins.dep_structs cimport dep_fun_args
cdef void dep_constant(double * x, ant_state* s, dep_fun_args* args)
cdef void dep_exdecay(double * x, ant_state* s, dep_fun_args* args)
