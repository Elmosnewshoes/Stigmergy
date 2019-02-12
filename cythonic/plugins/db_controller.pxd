cdef class db_controller():
    # class attribute
    cdef readonly object db

    # class methods
    cdef readonly unsigned int new_sim_id(self,)
    cdef readonly void executemany(self,str qry, list values)
    cdef readonly void execute(self, str qry )
