# distutils: language = c++

import numpy as np
from cythonic.plugins.positions cimport point
from cythonic.plugins.dep_functions cimport dep_constant, dep_fun_args
from cythonic.core.ant cimport f_dep, ant_state
from libc.math cimport fmin as cmin

def deploy_times(deploy_method, n, **kwargs):
    " generate a list of time instances when an ant is to be deployed "
    if deploy_method == 'instant':
        " deploy all at time t==0 "
        return np.zeros(n,dtype = np.float)
    elif deploy_method == 'uniform_dist':
        " deploy times uniformly distributed between 0 and kwargs['t_max']"
        t = kwargs['t_max']*np.random.rand(n)
    elif deploy_method == 'gamma_dist':
        """ deploy times gamma distribution
        (https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.gamma.html)
        shape k = kwargs['k'], scale theta (inverse of 'steepness' of the pdf) = kwargs['teta']
        median at aprox k*theta distr"""
        t = np.random.gamma(size = n,shape = kwargs['k'],scale=kwargs['teta'] )
    else:
        " if deploy_method argument is not recognized, future work: raise exception "
        print(' You are not supposed to see this message! ')
    return np.sort(t-np.min(t))

cdef class Sim:
    def __init__(self, queen_args, domain_args, unsigned int n_agents, double dt, unsigned int steps,
                  deploy_style, deploy_timing,deploy_timing_args,  evap_rate):
        " bring the controller online "
        self.queen = Queen(n = n_agents, dt = dt, total_steps = steps, **queen_args)

        " initialize the domain"
        self.domain = Domain(**domain_args)

        " set simulation variables "
        self.t = 0.
        self.dt = dt
        if evap_rate < 0:
            "in case of constant evaporation, compensate for step duration "
            self.evap_rate = evap_rate**dt
        else:
            self.evap_rate = evap_rate
        self.foodcount = 0
        self.nestcount = 0
        self.steps = steps
        self.total_stepped = 0
        self.deploy_times = deploy_times(deploy_timing,n_agents, **deploy_timing_args)

        " initialize the ant states "
        xy, tetas = self.new_positions(deploy_style, n_agents,**{'R':self.domain.nest_radius, 'nest_loc':self.domain.nest_location})
        self.queen.initialize_states(xy,tetas)

        " check if the map needs manipulating "
        if evap_rate <0:
            self.domain.evaporate(&self.evap_rate)

    """ ===================== Calculate ant starting locations ===================== """
    def new_positions(self, deploy_style, n, **kwargs):
        " calculate the xy and theta starting point of an ant "
        cdef point p #start location
        cdef bint in_bound = False #check ant is placed within domain boundaries
        xy = np.zeros([n,2], dtype = np.float)
        tetas = np.zeros(n,dtype=np.float)
        if deploy_style =='nest_radian':
            " all ants start aligned with a radian originating from the nest"
            x = kwargs['nest_loc']['x']
            y = kwargs['nest_loc']['y']
            R = kwargs['R']
            for i in range(n):
                in_bound = False
                while in_bound == False: #keep trying until suitable deploy location is found
                    # expect nest location [nest_loc] and radius [R] in kwargs
                    teta = np.random.rand()*2*np.pi
                    # xy[i,0] = x+np.cos(teta)*R
                    # xy[i,1] = y+np.sin(teta)*R
                    p.x = x+np.cos(teta)*R
                    p.y = y+np.sin(teta)*R
                    in_bound = self.domain.check_bounds(&p)

                # store candidate deploy position
                xy[i,0] = p.x
                xy[i,1] = p.y
                tetas[i] = teta*180/np.pi

        elif deploy_style == 'different':
            " placeholder for different deploy tactics "
            print(' needs implementing ')
        else:
            " if deploy_style argument is not recognized, future work: raise exception "
            print(' You are not supposed to see this message! ')
        return xy, tetas



    """ ===================== Additional initializations ===================== """
    cdef void set_depositing(self, str fun_type, dep_fun_args):
        " setup the functions for dropping pheromone "
        self.queen.setup_ant_depositing(fun_type, dep_fun_args )

    def set_gaussian(self, double covariance, double significancy):
        " make sure there is a nice gaussian meshmap representing a single deposition of pheromone "
        self.domain.init_gaussian(covariance = covariance,significancy = significancy)


    """ ===================== Actual simulation ===================== """
    cdef readonly void sim_step(self):
        " do a step in the simulation, perform all simulation logic (boundary check e.g..)"
        if self.queen.count_active < self.queen.n:
            "not all ants have been deployed "
            self.expand_active() #deploy more ants


        cdef unsigned int i

        " do a round of pheromone depositing prior to stepping"
        for i in range(self.queen.count_active):
            # self.domain.add_pheromone(p = &self.queen.state_list[i].pos, Q = &self.queen.drop_quantity[i])
            self.domain.add_pheromone(p = &self.queen.state_list[i].dropper, Q = &self.queen.drop_quantity[i])

            # deposit the pheromone

        for i in range(self.queen.count_active):
            # target an ant
            self.queen.assign_state(&i)

            #sense (queen/domain)
            self.domain.fill_observations(&self.queen.pheromone_vec[i], &self.queen.state_list[i].left, &self.queen.state_list[i].right)

            # give ant a small nudge towards its target when antenna hovers over nest/food
            self.check_attractiveness(&self.queen.pheromone_vec[i])

            #step (queen)
            self.queen.step(&self.dt)

            #check conditions (boundary, nest and food)
            self.check_target()

            #poll the deposition quantity
            self.queen.agent.calc_quantity(&self.queen.drop_quantity[i])

        #evaporate (domain)
        self.domain.evaporate(&self.evap_rate)

        # update timestamp
        self.t+=self.dt

        # set stepcounter on the ant
        self.queen.agent.next_step()
        self.total_stepped += self.queen.count_active


    cdef void expand_active(self):
        " check if new agents are to be activated based on simulation time "
        cdef unsigned int i
        for i in range(self.queen.count_active, self.queen.n,1):
            if self.deploy_times[i] <= self.t:
                " deploy ant if its deploy time is  \seq (<=) than current time step"
                self.queen.deploy(i) # deploy ant by id

    cdef void check_attractiveness(self,observations * O):
        " logic for handling ant near nest/food "
        " make the nest and food a bit more attractive by a bit of feedback: "
        if (self.domain.check_pos(p = &self.queen.agent.state.left, foodbound = &self.queen.agent.state.foodbound)
            and not self.domain.check_pos(p = &self.queen.agent.state.right, foodbound = &self.queen.agent.state.foodbound)):
            " left sensor is at ant target, make right sensor observe less pheromone "
            O[0].rght=cmin(O[0].lft*0.5, O[0].rght)
        elif (not self.domain.check_pos(p = &self.queen.agent.state.left, foodbound = &self.queen.agent.state.foodbound)
            and self.domain.check_pos(p = &self.queen.agent.state.right, foodbound = &self.queen.agent.state.foodbound)):
            " right sensor is at ant target, make left sensor observe less pheromone "
            O[0].lft=cmin(O[0].rght*0.5, O[0].lft)


    cdef void check_target(self):
        """ Check the following:
            - Ant is out of bound? correct position
            - Ant is foodbound and at food? make nestbound and reverse
            - Ant is nestbound and at nest? make foodbound and reverse
        """
        " ===== WARNING: assumption, ant cannot go from out of bounds to nest/food in a single step ====="

        cdef bint foodbound = True
        cdef bint nestbound = False
        " check arrival at food or nest "
        cdef double dt = self.dt * 1 # small step to avoid trapping in food or nest due to rounding errors
        if self.domain.check_pos(p = &self.queen.agent.state.pos, foodbound = &foodbound):
            " ant body is at food "
            self.queen.agent.reverse()
            self.queen.agent.step(&dt)
            if self.queen.agent.state[0].foodbound == foodbound:
                # ant was also looking for food: do the counting magic
                self.queen.agent.state[0].foodbound = nestbound #toggle state
                self.foodcount +=1 #count
                self.queen.agent.state[0].time = 0. # reset agent internal timer


        elif self.domain.check_pos(p = &self.queen.agent.state.pos, foodbound = &nestbound):
            " ant body is at nest "
            self.queen.agent.reverse()
            self.queen.agent.step(&dt)
            if self.queen.agent.state[0].foodbound == nestbound:
                # ant was also looking for the nest: do the magic
                self.queen.agent.state[0].foodbound = foodbound #toggle state
                self.nestcount +=1 #count
                self.queen.agent.state[0].time = 0. # reset agent internal timer

        elif not self.domain.check_bounds(&self.queen.agent.state.pos):
            " change this 'elif' to 'if' when ant can go from out of bounds to nest/food in a single step"
            " ant is out of bounds "
            # make sure the ant position does not violate domain constraint
            self.domain.constraint(&self.queen.agent.state.pos)

            # set the ant state
            self.queen.agent.out_of_bounds(1)

            # update sensor locations
            self.queen.agent.set_sensors()

        else:
            " make sure out_of_bounds flag is false "
            self.queen.agent.out_of_bounds(0)

    # def calc_score(self):
    #     " calculate a dimensionless performance indicator "
    #     " R: distance between food and nest "
    #     " T: simulation time "
    #     " S: ant speed "
    #     " score: indicator of usefull distance covered compared to total distance capacity "
    #     R = np.linalg.norm(np.array([self.domain.food_location.x,self.domain.food_location.y])
    #         -np.array([self.domain.nest_location.x,self.domain.nest_location.y]))-(self.domain.nest_radius+self.domain.food_radius)
    #     T = self.steps*self.dt #duration in seconds
    #     S = self.queen.default_speed # ant speed in mm/second
    #     score = self.nestcount * R / (self.total_stepped * S * T) #minimum required distance per 'nestcount' divided by total disctance stepped
    #     # print(f"Distance between food and nest: {R} mm")
    #     # print(f"Simulation duration: {T} sec")
    #     # print(f"Ants move at {S} mm/sec")
    #     # print(f"Ant score: {score} [ants/mm/hr]")
    #     return score
