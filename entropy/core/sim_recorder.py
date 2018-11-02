import numpy as np
from sim import Sim
import sys
import sqlite3
from plugins.qry_vars import create_new_sim, insert_step, insert_stepupdates
from visualization import StigmergyPlot

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
    def __init__(self,simname,limits, ant_gain, deploy_args, domain_args, ant_constants,dt):
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
        var_dict['start_concentration'] = self.domain_args['start_concentration']
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
        # db_path = sys.path[0]+"/database/"
        # db_name = "stigmergy_database.db"
        self.db = sqlite3.connect(db_path+db_name)

    def insert_step(self,sim_id,step,execute = False):
        """ insert step into table 'sim_updates' and corresponding ant positions
        into the 'ant_updates' table """
        " if execute is True, commit to database, else just append query "
        self.step_vars += insert_step['args'].format(step = step, sim_id = sim_id)
        for ant in self.Sim.Queen.ants:
            if ant.out_of_bounds:Q=0
            else: Q = ant.drop_quantity
            self.stepupdate_vars += insert_stepupdates['args'].format(step=step,
                                                                      ant_id = ant.id,
                                                                       x=ant.pos.x,
                                                                       y= ant.pos.y,
                                                                       teta = ant.azimuth,
                                                                       Q = Q)
        if execute:
            "send queries to database and reset the placeholder strings"
            cursor = self.db.cursor()
            try:
                cursor.execute(insert_step['qry'].format(args=self.step_vars[:-1]))
            except Exception as error:
                self.db.close()
                raise error
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
        self.Sim.start_sim(**self.deploy_args)# initialize the simulation
        self.Sim.Domain.set_target_pheromone(Q = 100*self.Sim.n_agents) #target pheromone total
        self.Sim.Domain.evaporate() #set base level
        self.Sim.Domain.update_pheromone() # idem
        self.Sim.gradient_step(gain = ant_gain,dt = self.dt, noise=ant_gain*1e-3*2*1.75) #deploy ants
        " Loop the simulation"
        for i in range(n_steps):
            if (i+1)%record_frequency==0  and i>0 and record_frequency!=-1:
                # self.insert_step(sim_id,i,True)
                self.insert_step(sim_id,i,True)
            else:
                self.insert_step(sim_id,i,False)
            self.Sim.deposit_pheromone( True)
            self.Sim.Domain.evaporate()
            self.Sim.Domain.update_pheromone()
            self.Sim.gradient_step(gain = ant_gain,dt = self.dt, noise=ant_gain*1e-3*2*1.75)

    def visualize_results(self):
        P = StigmergyPlot(self.Sim.Domain.Map,n=10)
        P.draw_stigmergy(self.Sim.Domain.Map.map)
        R_nest = np.empty((0,2)) #visualize the nest location
        R_food = np.empty((0,2)) #visualize the food location
        for i in range(0,360,10):
            " Create scatter of the edges of nest and food source "
            R_nest = np.vstack((R_nest,np.array(self.Sim.Domain.nest_location.vec)
                                +T_matrix(i).dot([self.Sim.Domain.nest_radius,0])))
            R_food = np.vstack((R_food,np.array(self.Sim.Domain.food_location.vec)
                                +T_matrix(i).dot([self.Sim.Domain.food_radius,0])))
        P.draw_scatter(x = R_nest[:,0],y=R_nest[:,1],name='nest')
        P.draw_scatter(x = R_food[:,0],y=R_food[:,1],name='food')
        # P.draw_entropy(S.entropy)
        P.draw()
        print("{} ants found food and {} returned".format(self.Sim.foodcount,
                                                          self.Sim.nestcount))
        P.hold_until_close()


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
            'deploy_location': 'nest'}

domain_dict = {'size': limits,
                'pitch': 1,
                'nest':{'location': nest,'radius':100},
                'food':{'location': food,'radius':100},
                'start_concentration':1}
ant_constants = {'speed': 15,
                'l': 10,
                'antenna_offset': 30,
                'limits': limits,
                'drop_quantity':Q}


def test_SimRecorder():
    sim_id=0
    S = SimRecorder(simname = 'simplesim',
                    limits = limits,
                    ant_gain = ant_gain,
                    deploy_args = deploy_dict,
                    domain_args = domain_dict,
                    ant_constants = ant_constants,
                    dt = 1)
    S.connect_db(db_path = sys.path[0]+"/database/",
                 db_name = "stigmergy_database.db")
    sim_id = S.insert_new_sim()
    S.record_gradient_sim(1000,500,sim_id)
    S.close_db()

    S.visualize_results()

if __name__ == '__main__':
    test_SimRecorder()
