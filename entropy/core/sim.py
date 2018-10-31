from domain import Domain
from ant import Queen, lin_fun

class Sim:
    def __init__(self, dom_dict,ant_dict = {}):
        "Do the simulation thing"
        self.Domain = Domain(**dom_dict) # dom needs size, pitch, nest and food
        self.Queen = Queen()

        " Keep track of the simulation progress "
        self.sim_time = 0
        self.n_agents = 0
        self.all_deployed = False #boolean to see if all ants are active


    def parse_pheromone(self, lefts, rights):
        " Return list of pheromone concentration under left and right antenna "
        return [[Domain.probe_pheromone(left),
                Domain.probe_pheromone(right)]
                for left,right in zip(lefts,rights)]

    def start_sim(self,n_agents,sigma,deploy_method='instant'):
        " Make the sim environment, determine when ants are to deployed "
        if deploy_method=='instant':
            self.deploy_time = np.zeros(n_agents)
        self.Domain.Gaussian = D.init_gaussian(sigma)


    def gradient_step(self,gain, dt):
        " Gradient step, update map"
        "Check if ants need to be deployed"
        if Queen.n < self.n_agents:
            sum(self.deploy_time < self.sim_time)
        self.Queen.gradient_step(gain =, dt = dt)


def run():
    limits = [1000,1000]
    food = [750,500]
    nest = [250,500]
    ant_gain = 1
    n_ants = 10
    pheromone_variance = 5
    sim_dict = {'n_agnts': n_ants,
                'sigma': pheromone_variance,
                'deploy_method': 'instant'}
    domain_dict = {'size': [1000,1000],
                    'pitch': 1,
                    'nest':{'location': nest,'radius':50},
                    'food':{'location': food,'radius':50}}
    ant_constants = {'speed': 10,
                    'limits': [1000,1000],
                    'l': 10,
                    'antenna_offset': 45}
    S = Sim(domain_dict, ant_constants)

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


    run()
