# distutils: language = c++

from libcpp.vector cimport vector
from cythonic.plugins.sens_structs cimport observations
from cythonic.core.ant cimport Ant, ant_state


""" ============
    The queen is the controller of the ants (agents)
    It is encouraged to play 'Master of Puppets' while executing this class
    ============ """
cdef class Queen:
    def __cinit__(self,unsigned int n, ant_dict, double dt):
        " initialize the controller (Queen) "
        self.n = n # total number of agents
        state_list = new vector[ant_state](n) # reserve memory for a vector of states

        " sim settings "
        self.dt = dt

        " deploy a model for the agent, which accepts and modifies a state "
        self.agent = Ant(**ant_dict)

    cpdef readonly void deploy(self, ant_state s):
        " activate an ant "
        s.active = True # activate the ant
        self.state_list.push_back(s) # store the ant state
        self.count_active += 1 # count active ants

    cdef readonly void step_all(self,):
        " step all, else step specified "
        for i in range(self.count_active):
            " todo: sense on map"
            self.gradient_step(i, &self.pheromone_vec[i])


    cdef readonly void gradient_step(self, int ant_id, observations * Q):
        " do the gradient stepping on the agent "
        self.agent.set_state(&self.state_list[ant_id])
        self.agent.gradient_step(&self.dt, Q)


    cpdef readonly void print_pos(self):
        " print the position struct of all ant in the state vector "
        for i in range(self.state_list.size()):
            print(self.state_list[i].id,self.state_list[i].pos)




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
