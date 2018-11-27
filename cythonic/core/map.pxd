from cythonic.plugins.positions cimport point, index, map_range

cdef class Map:
    cdef:
        readonly double pitch
        readonly point dim
        readonly double[:,::1] map, mesh_x, mesh_y
        readonly index lim

    " methods "
    cdef readonly unsigned long to_grid(self,double * x)
    cdef readonly double to_mm(self,unsigned long * x)
    cdef readonly map_range span(self,unsigned long *, unsigned long *,double*)
cdef class MeshMap(Map):
    cdef double i
cdef class GaussMap(Map):
    cdef double radius, volume, peak
