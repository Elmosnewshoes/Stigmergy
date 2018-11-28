cdef class RNG():
    cdef:
        double t,beta
    cdef readonly double rand(self)
    cdef readonly void add_t(self,double dt)
    cdef readonly double exp_rand(self)
