from cythonic.plugins.positions import point

cdef class MeshMap:
    cdef public double resolution
    cdef public double[2] dim
