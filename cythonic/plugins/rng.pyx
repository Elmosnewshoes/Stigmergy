cimport cython
from libc.stdlib cimport rand as crand, RAND_MAX
from libc.math cimport exp as cexp, log as cln

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
cdef class RNG():
    " random number generator, approx 40-50x faster than numpy "
    cdef double rand(self):
        return <double>crand()/(<double>RAND_MAX+1.)

    cdef readonly void add_t(self,double dt):
        self.t-=dt

    cdef readonly double exp_rand(self):
        " beta = 1/gamma --> CDF^-1 := -1/gamma*log(1-X)"
        return -self.beta*cln(1.-self.rand())

    def __cinit__(self,double gamma = 1):
        self.t = 0 #countdown timer
        self.beta = 1/gamma #preload devisor
