from domain import Domain
from ant import Queen, lin_fun
import numpy as np
from visualization import StigmergyPlot
from plugins.helper_functions import lin_fun,class_tuple2nparray

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

    def start_sim(self,n_agents,sigma,sens_function,deploy_location,
                  deploy_method='instant'):
        " Make the sim environment, determine when ants are to deployed "
        if deploy_method=='instant':
            self.deploy_time = np.zeros(n_agents)
        self.Domain.Gaussian = self.Domain.init_gaussian(sigma)
        self.n_agents = n_agents
        if sens_function == 'linear':
            self.sens_function = lin_fun
        self.deploy_location = deploy_location

    def deploy_params(self, n):
        " return pair of start positions and angles for newly deployed ants "
        if self.deploy_location=='nest': #all ants deploy at the edge of the nest
            R = self.Domain.nest_radius
            nest = self.Domain.nest_location.vec
            teta = np.random.rand(n)*2*np.pi
            start_locs = nest+np.dstack((np.cos(teta)*R,np.sin(teta)*R))[0]
        return start_locs, np.degrees(teta)

    def check_target(self):
        " check if ant is at target and should reverse "
        for i in range(self.Queen.n):
            with self.Queen.ants[i] as ant:
                if ant.foodbound and self.Domain.inrange(ant.pos,'food'):
                    self.foodcount+=1
                    ant.reverse()
                elif not ant.foodbound and self.Domain.inrange(ant.pos,'nest'):
                    self.nestcount+=1
                    ant.reverse()


    def gradient_step(self,gain, dt, noise):
        " Gradient step, update map"
        "Check if ants need to be deployed"
        if self.Queen.n < self.n_agents:
            " Deploy (more) agents "
            n = np.sum(self.deploy_time <= self.sim_time)
            start_locs, start_angles = self.deploy_params(n)
            self.Queen.deploy(start_locs, start_angles, self.ant_dict)
        Q = self.parse_pheromone(self.Queen.left, self.Queen.right)
        self.Queen.observe_pheromone(self.sens_function,Q,{'noise':noise})
        self.Queen.gradient_step(gain = gain, dt = dt)
        # self.Queen.update_positions()
        self.check_target()

    def deposit_pheromone(self, tau, by_volume = False):
        " deposit quantity tau pheromone at the ant locations "
        for i in range(self.Queen.n):
            if not self.Queen.ants[i].out_of_bounds:
                self.Domain.local_add_pheromone(self.Queen.ants[i].pos, tau, by_volume)

class SimRecorder():
    def __init__(self,simname,limits, ant_gain, sim_args, domain_args, ant_constants):
        " Record a simulation "
        Sim = Sim(dom_dict = domain_args, ant_dict= ant_constants)
        self.deploy_args = sim_args
        self.domain_args = domain_args
        self.domain_args['limits'] = limits

    def run_gradient_sim(self, n_steps, dt):
        " "
        self.Sim.start_sim(**self.deploy_args)# initialize the simulation
        self.Sim.Domain.set_target_pheromone(Q = 100*n_ants) #target pheromone total
        self.Sim.Domain.evaporate() #set base level
        self.Sim.Domain.update_pheromone() # idem

class SimPlayer():
    def __init__(self):
        " Playback a recorded simulation "

limits = [1000,500]
food = [850,250]
nest = [150,250]
ant_gain = 15
n_ants = 80
pheromone_variance = 7

deploy_dict = {'n_agents': n_ants,
            'sigma': pheromone_variance,
            'deploy_method': 'instant',
            'sens_function':'linear',
            'deploy_location': 'nest'}

domain_dict = {'size': limits,
                'pitch': 1,
                'nest':{'location': nest,'radius':100},
                'food':{'location': food,'radius':100},
                'start_concentration':1}
ant_constants = {'speed': 15,
                'l': 10,
                'antenna_offset': 30,
                'limits': limits}

def run():
    S = Sim(domain_dict, ant_constants)
    print(S.Domain.Map.map.sum())


def sim_only():
    S = Sim(domain_dict, ant_constants,)
    S.start_sim(**deploy_dict)# initialize the simulation
    S.Domain.set_target_pheromone(Q = 100*n_ants) #target pheromone total
    S.Domain.evaporate() #set base level
    S.Domain.update_pheromone() # idem
    dt =1
    n=1000
    for i in range(n):
        # print(f"Round {i}")
        # S.entropy.append(S.Domain.Map.entropy(S.Domain.target_pheromone))
        S.gradient_step(gain = ant_gain,dt = dt, noise=ant_gain*1e-3*1.75)
        S.deposit_pheromone(.005*dt, True)
        S.Domain.evaporate()
        S.Domain.update_pheromone()

    P = StigmergyPlot(S.Domain.Map,n=n)
    P.draw_stigmergy(S.Domain.Map.map)
    # P.draw_entropy(S.entropy)
    P.draw()
    print("{} ants found food and {} returned".format(S.foodcount,S.nestcount))
    P.hold_until_close()
    # print(S.entropy)




if __name__ == '__main__':
    """ === Ant simulation steps: ===
    Domain:
        1: deploy domain
        2: set target pheromone level
        3: set the gaussian for pheromone deposition
    Ants:
        1:Deploy ants

    == Step ==
        1: sense pheromone
        2: perform gradient step
        3: update the map

    ================================== """

    # run()
    sim_only()
