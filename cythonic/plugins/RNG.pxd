cdef extern from "/home/bram/ANTS/cythonic/plugins/mt19937.h" namespace "mtrandom":
    unsigned int N
    cdef cppclass MT_RNG:
        MT_RNG()
        MT_RNG(unsigned long s)
        MT_RNG(unsigned long init_key[], int key_length)
        void init_genrand(unsigned long s)
        unsigned long genrand_int32()
        double genrand_real1()
        double operator()()

cdef class RNG:
    cdef MT_RNG *_thisptr
    cpdef unsigned long randint(self)
    cpdef double rand(self)
