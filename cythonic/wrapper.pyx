from cythonic.core.ant cimport cube
from cythonic.core.ant cimport Ant
from cythonic.plugins.positions cimport point
from cythonic.plugins.functions cimport rot_matrix
import numpy as np

from cythonic.plugins.sens_functions cimport lin

cdef double sens_fun(str fun_type, double *x):
    if fun_type=='linear':
        return lin(x)
def sens(str fun_type, double x):
    return sens_fun(fun_type,&x)

def cube_wrapped(x):
    return cube(x)


def pnt(x,y):
    p = point(x,y)
    return p

cdef class pyAnt(Ant):
    def attributes(self):
        return [attr for attr in dir(self)
                  if not attr.startswith('__') and not attr == 'attributes']
    def chck_bnds(self):
        return self.correct_bounds()
    def return_positions(self):
        return [np.array(self._pos.xy),
            np.array(self._left.xy),
            np.array(self._right.xy)]

def rotate(teta):
    return rot_matrix(teta)
