from cythonic.core.domain cimport Domain

cdef class SimPlayer:
    cdef:
        readonly object db, ant_steps
        readonly unsigned int n_agents, count_active
        readonly unsigned int id, cur_step,steps
        double evap_rate, dt
        double max_pheromone_level
        Domain domain

        readonly double ant_size, d, sens_offset
        double[:,::] positions
        double[:,::] droppers
        double[:] headings
        double[:,::] lefts
        double[:,::] rights

        unsigned int[:] steplist
        double[:] entropy
        unsigned int[:] nestcount

    cdef void step(self, unsigned int stepnr)
    cpdef void next(self,)
    cpdef void renew(self,)
    cdef void reset_vectors(self)
