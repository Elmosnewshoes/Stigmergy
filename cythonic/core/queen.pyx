# from cythonic.core.ant cimport Ant
# import numpy as np
# from cythonic.plugins.positions cimport ant_state
# from time import time
# cimport cython
#
#
# @cython.cdivision(True)
# @cython.wraparound(False)
# @cython.boundscheck(False)
# @cython.nonecheck(False)
# cdef class queen():
#     " wrapper for the ant class, difficulties casting list of ants to c-objects :("
#     def __cinit__(self,long n):
#         self.n = n
#         self.ants = []
#         self.count_active = 0
#
#     cpdef void deploy(self, ):
#         ant_dict = {'speed' : 10, 'gain' : 2, 'l' : 5, 'sens_offset' : 45,
#           'limits' :np.array([10,10],dtype=np.float_),'q' : 1.5, 'return_factor' :1,
#           'drop_fun' : 'exp_decay', 'drop_beta' : .5, 'rng_gamma':2}
#         cdef int i
#         cdef Ant a
#         for i in range(self.n):
#             a = Ant(id = i,**ant_dict)
#             self.ants.append(a)
#
#     cdef readonly void activate(self, ant_state s):
#         " activate next ant "
#         with self.ants[self.count_active] as ant:
#             ant.activate(s)
#         self.count_active+=1
#
#
#     cpdef void reverse(self):
#         for ant in self.ants:
#             if ant.active:
#                 ant.reverse()
#
#     cpdef void gradient_step(self,double dt, str observe_fun, double[:] Q):
#         "Gradient step wrapper"
#         for ant in self.ants:
#             if ant.active:
#                 ant.gradient_step(dt,observe_fun,Q)
#
#     cpdef void observe_pheromone(self,str observe_fun, double[:] Q):
#         "observe pheromone wrapper"
#         # print(Q)eposit quantity time constant
#         for i in range(self.n):
#             with self.ants[i] as ant:
#                 if ant.active:
#                     ant.observe_pheromone(observe_fun,Q[i])
