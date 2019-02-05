from cythonic.core.sim_controller cimport Sim
from cythonic.plugins.db_controller cimport db_controller

cdef class sim_recorder(Sim):
    cdef db_controller db
    cdef: # class attributes
        readonly unsigned int update_interval
        readonly unsigned int id
        readonly str pending_qry
        readonly list qry_args
        readonly dict ant_dict, queen_dict, domain_dict,  sim_dict
    cdef: # class methods
        readonly void flush_resultset(self,)
        readonly void extract_antstate(self, unsigned int step)
        readonly dict run_sim(self, bint record)
