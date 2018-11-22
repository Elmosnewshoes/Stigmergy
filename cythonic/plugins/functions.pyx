cimport numpy as np
import numpy as np
from libc.math cimport sin as csin,cos as ccos
from cythonic.plugins.positions cimport point
from libc.math cimport M_PI as PI

cdef double deg(double *rad):
    return rad[0]*180/PI

cdef double rad(double * deg):
    return deg[0]*PI/180

DTYPE = np.float_
cdef np.ndarray rot_matrix(double teta_deg):
    " return a transformation matrix [cos(teta), -sin(teta);sin(teta), cos(teta)]"
    cdef double teta = np.deg2rad(teta_deg)
    cdef np.ndarray T = np.array([[ccos(teta),-csin(teta)],[csin(teta),ccos(teta)]],dtype=DTYPE)
    return T

cdef point transform(double teta_deg, double *arm, double[2]* xy):
    " return location of a point based on: [x;y] = T*[arm;0]+offset"
    cdef double teta = rad(&teta_deg)
    cdef point result = point(xy[0][0]+ccos(teta)*arm[0],xy[0][1]+csin(teta)*arm[0])
    return result
