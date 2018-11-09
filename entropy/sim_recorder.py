import numpy as np
from core.sim import Sim
import sys
import sqlite3
from core.plugins.qry_vars import create_new_sim, insert_stepupdates
from core.visualization import StigmergyPlot
from core.plugins.helper_functions import T_matrix, circle_scatter

class SimRecorder():
    """ === Ant simulation steps: ===
    Domain:
        1: deploy domain
        2: set target pheromone level
        3: set the gaussian for pheromone deposition
    Ants:
        1:Deploy ants

    == Run, for all agents ==
        1: sense pheromone
        2: perform gradient step
        3: update the map

    ================================== """
    def __init__(self,simname,limits, deploy_args, domain_args, ant_constants,dt):
        " Record a simulation "
        self.Sim = Sim(dom_dict = domain_args, ant_dict= ant_constants)
        self.deploy_args = deploy_args
        self.domain_args = domain_args
        self.ant_constants = ant_constants
        self.domain_args['limits'] = limits
        self.dt = dt

        # some query values
        self.step_vars = ''
        self.stepupdate_vars = ''


    def insert_new_sim(self,):
        " start logging of sim in sqlite database "
        var_dict = {key:value for key,value in self.deploy_args.items()}
        for key,value in self.ant_constants.items(): var_dict[key]=value
        var_dict['pitch']=self.domain_args['pitch']
        var_dict['dt']=self.dt
        var_dict['nest_location'] = self.domain_args['nest']['location']
        var_dict['nest_radius'] = self.domain_args['nest']['radius']
        var_dict['food_location'] = self.domain_args['food']['location']
        var_dict['food_radius'] = self.domain_args['food']['radius']
        cursor = self.db.cursor()
        try:
            cursor.execute(create_new_sim.format(**var_dict))
            id = cursor.lastrowid
            self.db.commit()
        except Exception as error:
            self.db.close()
            raise error
        return id

    def connect_db(self,db_path,db_name):
        self.db = sqlite3.connect(db_path+db_name)

    def insert_step(self,sim_id,step,execute = False):
        """ insert step into table 'sim_updates' and corresponding ant positions
        into the 'ant_updates' table """
        " if execute is True, commit to database, else just append query "
        # self.step_vars += insert_step['args'].format(step = step, sim_id = sim_id)
        for ant in self.Sim.Queen.ants:
            if ant.out_of_bounds:Q=0
            else: Q = ant.drop_quantity
            args = {'sim_id': sim_id,'step':step,'ant_id':ant.id,'x':ant.pos.x,
                    'y': ant.pos.y,'teta':ant.azimuth,'Q': Q}
            self.stepupdate_vars += insert_stepupdates['args'].format(**args)
        if execute:
            "send queries to database and reset the placeholder strings"
            cursor = self.db.cursor()
            try:
                cursor.execute(insert_stepupdates['qry'].format(
                    args = self.stepupdate_vars[:-1]))
            except Exception as error:
                self.db.close()
                raise error

            " cleanup "
            self.db.commit()
            self.step_vars = ''
            self.stepupdate_vars = ''


    def close_db(self):
        self.db.close()

    def record_gradient_sim(self, n_steps,record_frequency,sim_id):
        """ Run a gradient based simulation """
        " Initialize the simulation "
        # h = []
        # t = []
        self.Sim.start_sim(**self.deploy_args)# initialize the simulation
        self.Sim.gradient_step(dt = self.dt) #deploy ants
        " Loop the simulation"
        for i in range(n_steps):
            if (i+1)%record_frequency==0  and i>0 and record_frequency!=-1:
                # self.insert_step(sim_id,i,True)
                self.insert_step(sim_id,i,True)
            elif record_frequency !=-1:
                self.insert_step(sim_id,i,False)
            self.Sim.gradient_step(dt = self.dt)
            self.Sim.deposit_pheromone( )
            self.Sim.Domain.evaporate()
            # if i%10 ==0:
            #     h.append(self.Sim.Domain.Map.entropy())
            #     t.append(i)
        # print(h)

    def visualize_results(self):
        P = StigmergyPlot(self.Sim.Domain.Map,n=10)
        P.draw_stigmergy(self.Sim.Domain.Map.map)
        scat_nest = circle_scatter(self.Sim.Domain.nest_location.vec, self.Sim.Domain.nest_radius)
        scat_food = circle_scatter(self.Sim.Domain.food_location.vec, self.Sim.Domain.food_radius)
        P.draw_scatter(x = scat_nest[:,0],y=scat_nest[:,1],name='nest')
        P.draw_scatter(x = scat_food[:,0],y=scat_food[:,1],name='food')
        # P.draw_entropy(S.entropy)
        P.draw()
        print("{} ants found food and {} returned".format(self.Sim.foodcount,
                                                          self.Sim.nestcount))
        P.hold_until_close()


limits = [1000,500]
food = [750,250]
nest = [250,250]
ant_gain = 10
noise_gain = .08#5/(180/np.pi)
n_ants = 80
pheromone_variance = 15
Q=2
drop_fun = 'exp_decay'
return_factor = 1.5

deploy_dict = {'n_agents': n_ants,
            'sigma': pheromone_variance,
            'deploy_method': 'instant',
            'sens_function':'linear',
            'deploy_location': 'nest',
            'target_pheromone_volume':1001**2}

domain_dict = {'size': limits,
                'pitch': 1,
                'nest':{'location': nest,'radius':75},
                'food':{'location': food,'radius':75}}
ant_constants = {'speed': 15,
                'l': 10,
                'antenna_offset': 45,
                'limits': limits,
                'drop_quantity':Q,
                'gain':ant_gain,
                'beta':2, #exponential noise function
                'noise_gain':noise_gain,#1e-3*2*1.75}
                'drop_fun':drop_fun,
                'return_factor':return_factor}


def test_SimRecorder():
    S = SimRecorder(simname = 'simplesim',
                    limits = limits,
                    deploy_args = deploy_dict,
                    domain_args = domain_dict,
                    ant_constants = ant_constants,
                    dt = 1)
    S.connect_db(db_path = sys.path[0]+"/core/database/",
                 db_name = "stigmergy_database.db")
    sim_id = S.insert_new_sim()
    S.record_gradient_sim(n_steps = 3000,record_frequency=500,sim_id=sim_id)
    S.close_db()

    S.visualize_results()

if __name__ == '__main__':
    test_SimRecorder()
