from cythonic.core.domain cimport Domain

cdef class SimPlayer:
    cdef:
        readonly object db, steps
        readonly unsigned int n_agents, count_active
        readonly unsigned int id, cur_step
        double evap_rate
        Domain domain

        readonly double ant_size, sens_offset
        double[:,::] positions
        double[:] headings
        double[:,::] lefts
        double[:,::] rights

    cdef void step(self, unsigned int stepnr)
    cpdef void next(self,)
