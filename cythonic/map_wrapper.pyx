from cythonic.core.map cimport MeshMap
from cythonic.plugins.positions cimport point, index



cdef class MMap(MeshMap):
    " inherit the meshmap and publish its methods to python "
    def attributes(self):
        return [attr for attr in dir(self)
                  if not attr.startswith('__') and not attr == 'attributes']
    def rounded(self, double x):
        return self.to_grid(&x)
