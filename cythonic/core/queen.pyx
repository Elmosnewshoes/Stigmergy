# distutils: language = c++
cimport cython
from cythonic.plugins.sens_structs cimport observations
from cythonic.plugins.sens_functions cimport telegraph_noise
from cythonic.core.ant cimport Ant, ant_state
import numpy as np

""" ============
    The queen is the controller of the ants (agents)
    It is encouraged to play 'Master of Puppets' while executing this class
    ============ """
cdef class Queen:
    def __cinit__(self,unsigned int n, dict ant_dict, double dt, double default_speed,
        str noise_type, double noise_parameter, unsigned int total_steps):
        " initialize the controller (Queen) "
        self.n = n # total number of agents
        self.count_active = 0 #keep track of activated ants
        self.total_steps = total_steps

        " sim settings "
        self.dt = dt
        self.default_speed = default_speed
        self.noise_type = noise_type
        self.noise_parameter = noise_parameter

        " deploy a model for the agent, which accepts and modifies a state "
        self.agent = Ant(**ant_dict)


        " populate the pheromone vector "
        cdef observations O = {'lft': 0.,'rght':0.}
        for i in range(self.n):
            self.pheromone_vec.push_back(O)

        " populate a memview for quantity pheromone dropped "
        self.drop_quantity = np.ones(n,dtype = np.float)

    cdef void setup_ant_depositing(self,str fun_type, dep_fun_args args ):
        """ set the dropping function and its arguments, initialize the
            drop quantity q=f(t) -> f(0)==q <- drop_quantity"""
        self.agent.set_actuator_args(fun = fun_type, args = args )
        for element in self.drop_quantity:
            element = args.q


    cdef readonly void step(self, double * dt):
        " perform step on active agent "
        self.agent.gradient_step(dt, &self.pheromone_vec[self.agent.state[0].id])

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
        s.time = 0.
        s.noise_vec = self.noise_vec()

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
        # warning, not being used in the sim, set next_step manually in the sim
        " step all ants "
        for i in range(self.count_active):
            self.assign_state(&i)
            self.gradient_step( &self.pheromone_vec[i])
        self.agent.next_step()

    cdef readonly void assign_state(self,unsigned int *ant_id):
        " set the state of the agent "
        self.agent.set_state(&self.state_list[ant_id[0]])

    cdef readonly void gradient_step(self, observations * Q):
        " do the gradient stepping on the agent "
        self.agent.gradient_step(&self.dt, Q)

    cdef vector[double] noise_vec(self):
        " make noise vector for ant state at initialization "
        cdef vector[double] noise
        if self.noise_type == 'white':
            " stream of white gaussian noise "
            for element in np.random.normal(0,1,self.total_steps):
                noise.push_back(element)

        elif self.noise_type == 'uniform':
            " stream of uniformly distributed noise from U(-1,1) "
            for element in 2*(np.random.rand(self.total_steps)-.5):
                noise.push_back(element)
        elif self.noise_type == 'telegraph':
            " telegraphic noise process bounded between [-1,1] "
            noise = telegraph_noise(self.total_steps, dt = self.dt, beta = self.noise_parameter)
        return noise

    cpdef readonly void print_pos(self):
        " print the position struct of all ant in the state vector "
        for i in range(self.state_list.size()):
            print(f'# {self.state_list[i].id}: {self.state_list[i].pos} || theta: {self.state_list[i].theta}')
            # print(self.state_list[i].id,self.state_list[i].pos, self.state_list[i])
