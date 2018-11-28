cdef class queen():
    " attributes "
    cdef list ants
    cdef unsigned int n

    "CPython methods "
    cpdef void deploy(self)
    cpdef void reverse(self)
    cpdef void gradient_step(self,double dt, str observe_fun, double[:] Q)
    cpdef void observe_pheromone(self,str observe_fun, double[:] Q)
