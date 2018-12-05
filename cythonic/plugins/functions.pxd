from cythonic.plugins.positions cimport point
cimport numpy as np

cdef double deg(double *rad)
cdef np.ndarray rot_matrix(double teta_deg)
cdef point transform(double, double*, point *)
