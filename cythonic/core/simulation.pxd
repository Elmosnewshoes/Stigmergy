from cythonic.core.sim_controller cimport Sim

cdef class live_sim(Sim):
    cdef object chart # the graph object
    cdef unsigned int interval #how often to refresh the graph

    " methods "
    cpdef void run_sim(self, unsigned int stride)
