from core.domain import Domain
from core.ant import Queen, lin_fun
import numpy as np
from core.plugins.helper_functions import lin_fun, T_matrix
from core.plugins.helper_classes import point


class Sim:
    def __init__(self, dom_dict,ant_dict):
        "Do the simulation thing"
        self.Domain = Domain(**dom_dict) # dom needs size, pitch, nest and food
        self.Queen = Queen()
        self.ant_dict = ant_dict
        self.deploy_location = 0 #initialize at start_sim
        self.sens_function = 0 # initialize at start_sim

        " Keep track of the simulation progress "
        self.n_agents = 0
        self.sim_time = 0
        self.foodcount = 0
        self.nestcount = 0
        self.all_deployed = False #boolean to see if all ants are active
        self.entropy = []


    def parse_pheromone(self, lefts, rights):
        " Return list of pheromone concentration under left and right antenna "
        return [[self.Domain.probe_pheromone(left),
                self.Domain.probe_pheromone(right)]
                for left,right in zip(lefts,rights)]

    def start_sim(self,n_agents,sigma,sens_function,deploy_location, target_pheromone_volume='',
                  deploy_method='instant'):
        " Make the sim environment, determine when ants are to deployed "
        if deploy_method=='instant':
            self.deploy_time = np.zeros(n_agents)
        self.Domain.Gaussian = self.Domain.init_gaussian(sigma)
        self.Domain.set_target_pheromone(target_pheromone_volume)
        self.Domain.evaporate() #start with the correct amount of pheromone
        # self.Domain.update_pheromone()
        self.n_agents = n_agents
        if sens_function == 'linear':
            self.sens_function = lin_fun
        self.deploy_location = deploy_location

    def deploy_params(self, n):
        " return pair of start positions and angles for newly deployed ants "
        if self.deploy_location=='nest': #all ants deploy at the edge of the nest
            R = self.Domain.nest_radius+1
            nest = self.Domain.nest_location.vec
            teta = np.random.rand(n)*2*np.pi
            start_locs = nest+np.dstack((np.cos(teta)*R,np.sin(teta)*R))[0]
        return start_locs, np.degrees(teta)

    def place_ant(self,ant_pos, R, base):
        " Reposition the ant when it has reached either the food or nest "
        if ant_pos.x==base.x:
            ant_pos.x+=1e-6 #avoid devison by 0
        teta = np.arctan((ant_pos.y-base.y)/(ant_pos.x-base.x))
        if ant_pos.x < base.x: teta+=np.pi
        return point(*(base.vec+np.dstack((np.cos(teta)*R,
                                           np.sin(teta)*R))[0][0])),np.degrees(teta)

    def check_target(self):
        " check if ant is at target and should reverse "
        for i in range(self.Queen.n):
            with self.Queen.ants[i] as ant:
                if self.Domain.inrange(ant.pos,'food'):
                    if ant.foodbound:
                        self.foodcount+=1
                        ant.foodbound = False
                    # ant.reverse()
                    ant.pos, ant.azimuth = self.place_ant(ant.pos,self.Domain.food_radius,self.Domain.food_location)
                elif self.Domain.inrange(ant.pos,'nest'):
                    if not ant.foodbound:
                        self.nestcount+=1
                        ant.foodbound = True
                    # ant.reverse()
                    ant.pos, ant.azimuth = self.place_ant(ant.pos,self.Domain.nest_radius,self.Domain.nest_location)
                # elif self.Domain.inrange(ant.pos,'food') or self.Domain.inrange(ant.pos,'nest'):
                #     ant.reverse(change_objective= False)


    def gradient_step(self,gain, dt, noise):
        " Gradient step, update map"
        "Check if ants need to be deployed"
        Q = self.parse_pheromone(lefts = [ant.sensors['left'] for ant in self.Queen.ants],
                                 rights = [ant.sensors['right'] for ant in self.Queen.ants])
        self.Queen.observe_pheromone(self.sens_function,Q,{'noise':noise})
        self.Queen.gradient_step(gain = gain, dt = dt)
        # self.Queen.update_positions()
        self.check_target()

        if self.Queen.n < self.n_agents:
            " Deploy (more) agents "
            n = np.sum(self.deploy_time <= self.sim_time)
            start_locs, start_angles = self.deploy_params(n)
            self.Queen.deploy(start_locs, start_angles, self.ant_dict)

    def deposit_pheromone(self):
        " deposit quantity tau pheromone at the ant locations "
        for i in range(self.Queen.n):
            if not self.Queen.ants[i].out_of_bounds:
                self.Domain.local_add_pheromone(self.Queen.ants[i].pos,
                                                self.Queen.ants[i].drop_quantity)



def run():
    limits = [1000,500]
    food = [750,250]
    nest = [250,250]
    ant_gain = 10
    n_ants = 80
    pheromone_variance = 12
    Q=.0005

    deploy_dict = {'n_agents': n_ants,
                'sigma': pheromone_variance,
                'deploy_method': 'instant',
                'sens_function':'linear',
                'deploy_location': 'nest',
                'target_pheromone_volume':100*n_ants}

    domain_dict = {'size': limits,
                    'pitch': 1,
                    'nest':{'location': nest,'radius':100},
                    'food':{'location': food,'radius':100}}
    ant_constants = {'speed': 15,
                    'l': 10,
                    'antenna_offset': 30,
                    'limits': limits,
                    'drop_quantity':Q}
    S = Sim(domain_dict, ant_constants)
    print(S.Domain.Map.map.sum())



if __name__ == '__main__':
    run()
