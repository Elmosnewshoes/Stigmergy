from cythonic.plugins.positions cimport point, index

cdef class MeshMap:
    cdef:
        readonly double pitch
        readonly point dim
        readonly double[:,::1] map
        readonly index lim

    " methods "
    cdef readonly unsigned long to_grid(self,double * x)
    cdef readonly double to_mm(self,unsigned long * x)
