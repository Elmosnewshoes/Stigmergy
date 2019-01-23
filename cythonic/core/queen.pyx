# distutils: language = c++
cimport cython
from libcpp.vector cimport vector
from cythonic.plugins.sens_structs cimport observations
from cythonic.core.ant cimport Ant, ant_state


""" ============
    The queen is the controller of the ants (agents)
    It is encouraged to play 'Master of Puppets' while executing this class
    ============ """
cdef class Queen:
    def __cinit__(self,unsigned int n, ant_dict, double dt,default_speed = 5.):
        " initialize the controller (Queen) "
        self.n = n # total number of agents
        self.count_active = 0 #keep track of activated ants

        " sim settings "
        self.dt = dt
        self.default_speed = default_speed

        " deploy a model for the agent, which accepts and modifies a state "
        self.agent = Ant(**ant_dict)

        " populate the pheromone vector "
        cdef observations O = {'lft': 0.,'rght':0.}
        for i in range(self.n):
            self.pheromone_vec.push_back(O)


    cdef readonly ant_state generate_state(self, point p, double theta):
        " generate a state struct for an ant "
        cdef ant_state s
        s.v = self.default_speed
        s.pos = p
        s.theta = theta
        s.id = self.state_list.size()
        s.foodbound = True
        s.out_of_bounds = False
        s.active = False
        s.rng_timer = 0.
        s.time = 0.

        return s

    @cython.boundscheck(True) #throws error when memview xy is not as long as self.n
    cpdef readonly void initialize_states(self,double[::,:] xy, double[:] theta):
        " deploy all the ant states based on received position tuple and angle "
        cdef unsigned int i
        cdef point p
        for i in range(self.n):
            p = point(xy[i,0],xy[i,1]) #cast array slice as point

            # generate the state and push it in the state vector
            self.state_list.push_back(self.generate_state(p,theta[i]))

    cdef readonly void deploy(self, unsigned int ant_id):
        " activate an ant "
        self.agent.set_state(&self.state_list[ant_id]) #assign state to ant
        self.agent.activate()
        self.agent.set_sensors() # let ant determine its sensor positions
        self.count_active += 1 # count active ants

    cdef readonly void step_all(self,):
        " step all, else step specified "
        for i in range(self.count_active):
            " todo: sense on map"
            self.assign_state(&i)
            self.gradient_step( &self.pheromone_vec[i])


    cdef readonly void assign_state(self,unsigned int *ant_id):
        " set the state of the agent "
        self.agent.set_state(&self.state_list[ant_id[0]])

    cdef readonly void gradient_step(self, observations * Q):
        " do the gradient stepping on the agent "
        self.agent.gradient_step(&self.dt, Q)


    cpdef readonly void print_pos(self):
        " print the position struct of all ant in the state vector "
        for i in range(self.state_list.size()):
            print(f'# {self.state_list[i].id}: {self.state_list[i].pos} || theta: {self.state_list[i].theta}')
            # print(self.state_list[i].id,self.state_list[i].pos, self.state_list[i])




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
