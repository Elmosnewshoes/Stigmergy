from cythonic.core.queen cimport Queen
from cythonic.core.ant cimport Ant, ant_state
from cythonic.core.domain cimport Domain
from cythonic.plugins.sens_structs cimport observations

cdef class Sim:
    # " class properties "
    cdef readonly Queen queen
    cdef readonly Domain domain

    cdef:
        readonly bint deployed #flag: all ants active == True
        readonly double[:] deploy_times #list of timers when ant should become active
        readonly double dt #simulation time step
        readonly double t #simulation time
        readonly double evap_rate
        public unsigned int foodcount
        public unsigned int nestcount
        public unsigned int steps
        public unsigned int total_stepped

    # " class methods "
    cdef:
        readonly void set_depositing(self, str fun_type, dep_fun_args)
        readonly void sim_step(self)
        readonly void expand_active(self)
        readonly void check_target(self)
        void check_attractiveness(self,observations * O)
