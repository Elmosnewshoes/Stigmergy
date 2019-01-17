#
# from cythonic.core.ant cimport Ant
# from cythonic.plugins.positions cimport point
# from cythonic.plugins.functions cimport rot_matrix
# import numpy as np
# from time import time
#
# from cythonic.plugins.sens_functions cimport lin
#
# cdef double sens_fun(str fun_type, double *x):
#     if fun_type=='linear':
#         return lin(x)
# def sens(str fun_type, double x):
#     return sens_fun(fun_type,&x)
#
#
#
# def pnt(x,y):
#     p = point(x,y)
#     return p
#
# cdef class pyAnt(Ant):
#     def attributes(self):
#         return [attr for attr in dir(self)
#                   if not attr.startswith('__') and not attr == 'attributes']
#     def chck_bnds(self):
#         return self.correct_bounds()
#     def return_positions(self):
#         return [np.array(self._pos),
#             np.array(self._left),
#             np.array(self._right)]
#     def return_observed(self,method, q):
#         cdef double[2] Q
#         Q[0] = q[0]
#         Q[1] = q[1]
#         self.observe(method,Q)
#         return np.array(self.q_observed)
#
#     def time_observe(self,int n):
#         " time observe function "
#         cdef double t, tic
#         cdef double[2] q
#         Q = np.random.rand(n,2)
#         tic = time()
#         for x in Q:
#             q[0]=x[0]
#             q[1]=x[1]
#             self.observe('linear', q)
#         return (time()-tic)*1e3 #mseconds
#
#     def time_step(self,int n):
#         cdef int x
#         cdef double dt = .1
#         cdef double tic =time()
#         for x in range(n):
#             self.step(&dt)
#         return (time()-tic)*1e3 #mseconds
#
#     def time_sensors(self,int n):
#         cdef int x
#         cdef double tic = time()
#         for x in range(n):
#             self.set_sensors()
#         return (time()-tic)*1e3 #mseconds
#
#     def time_iteration(self,int n):
#         cdef double tic, dt=.05
#         cdef double[2] q
#         Q = np.random.rand(n,2)
#         tic = time()
#         for x in Q:
#             q[0]=x[0]
#             q[1]=x[1]
#             # self.observe('linear', q)
#             self.gradient_step(dt, 'linear',q)
#         return (time()-tic)*1e3 #mseconds
#
#
#
#
# def rotate(teta):
#     return rot_matrix(teta)
