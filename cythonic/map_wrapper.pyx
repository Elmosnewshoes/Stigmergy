from cythonic.core cimport map
cdef class MeshMap(map.MeshMap):
    def attributes(self):
        return [attr for attr in dir(self)
                  if not attr.startswith('__') and not attr == 'attributes']
