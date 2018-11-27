cimport numpy as np
import numpy as np
from libc.math cimport sin as csin,cos as ccos
from cythonic.plugins.positions cimport point
from libc.math cimport M_PI as PI
cimport cython

cdef double deg(double *rad):
    return rad[0]*180/PI

cdef double rad(double * deg):
    return deg[0]*PI/180

ctypedef np.float64_t DTYPE_t

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
cdef np.ndarray[dtype=DTYPE_t,ndim=2] rot_matrix(double teta_deg):
    " return a transformation matrix [cos(teta), -sin(teta);sin(teta), cos(teta)]"
    cdef double teta = np.deg2rad(teta_deg)
    cdef np.ndarray T = np.array([[ccos(teta),-csin(teta)],[csin(teta),ccos(teta)]])
    return T

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
cdef point transform(double teta_deg, double *arm, point* xy):
    " return location of a point based on: [x;y] = T*[arm;0]+offset"
    cdef double teta = rad(&teta_deg)
    cdef point result = point(xy[0].x+ccos(teta)*arm[0],xy[0].y+csin(teta)*arm[0])
    return result
