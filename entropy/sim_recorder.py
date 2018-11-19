import numpy as np
from core.sim import Sim
import sys
import sqlite3
from core.plugins.helper_functions import append_dict
from core.plugins.qry_vars import *
from core.visualization import StigmergyPlot, Plotter
from core.plugins.helper_functions import T_matrix, circle_scatter
import pathlib

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
        dom_dict = {'size':self.domain_args['size'],
                    'nest_location': self.domain_args['nest']['location'],
                    'nest_radius': self.domain_args['nest']['radius'],
                    'food_location':self.domain_args['food']['location'],
                    'food_radius':self.domain_args['food']['radius'],
                    'pitch': self.domain_args['pitch']}
        cursor = self.db.cursor()
        try:
            cursor.execute(create_new_sim.format(dt=self.dt,**self.deploy_args))
            id = cursor.lastrowid
            cursor.execute(insert_ant_settings.format(sim_id=id,**self.ant_constants))
            cursor.execute(insert_domain_settings.format(sim_id=id,**dom_dict))
            self.db.commit()
        except Exception as error:
            self.db.close()
            raise error
        return id

    def connect_db(self,db_path,db_name):
        self.db = sqlite3.connect(db_path+db_name)

    def insert_results(self, result_dict):
        " Write the results to the database "
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_results.format(**result_dict))
            self.db.commit()
        except Exception as error:
            self.db.close()
            raise error

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

    def ant_things(self):
        " Do the ant moves (right sequence) "
        self.Sim.Domain.evaporate() #evaporate old step
        self.Sim.observe_pheromone() # sense the pheromone
        self.Sim.deposit_pheromone( ) # place new pheromone
        self.Sim.gradient_step(dt = self.dt) # move

    def init_results(self,record_frequency, n_steps,sim_id,H_steps,path,store_interval):
        H= []
        t= []
        record_frequency = np.min([record_frequency,n_steps])
        result = {} # result dictionary for database
        dirname = 'sim_{}/'.format(str(sim_id).zfill(5))
        if len(H_steps)>0:
            H_steps = np.multiply(H_steps,n_steps).astype(np.int32).tolist()
            H = np.zeros(len(H_steps)).tolist()
            t = np.dot(H_steps,self.dt).tolist() #time vec
        if path:
            " create the folder to store graphics and numpy arrays "
            pathlib.Path(path+dirname).mkdir(parents=True, exist_ok=True)
            store_interval = np.multiply(store_interval,n_steps).astype(np.int32).tolist()
        return H,t,record_frequency, result, dirname,H_steps,{}, store_interval

    def save_arrays(self, filepath,array_dict):
        " store np arrays to disk (compressed format)"
        np.savez_compressed(filepath,**array_dict)

    def record_gradient_sim(self, n_steps,record_frequency,sim_id,H_steps =[],
                            path = '',store_map_interval = []):
        """ Run a gradient based simulation """
        "setup some variables to store results"
        H,t,record_frequency, result, dirname, H_steps, Map_Dict, \
        store_map_interval = self.init_results(record_frequency,n_steps,sim_id,
                                               H_steps,path, store_map_interval)

        " Initialize the simulation "
        self.Sim.start_sim(**self.deploy_args)#
        result['start_entropy'] = self.Sim.Domain.Map.entropy() #logging

        " Loop the simulation"
        for i in range(n_steps+1):
            " Check the state of the domain"
            if i in H_steps:
                j = H_steps.index(i)
                H[j] = self.Sim.Domain.Map.entropy()

            " ants step "
            self.ant_things()

            " log the step "
            if i in store_map_interval:
                Map_Dict['MAP_t{}'.format(str(i).zfill(5))] = self.Sim.Domain.Map.map.copy()
            if (i+1)%record_frequency==0  and i>0 and record_frequency!=-1:
                self.insert_step(sim_id,i,True)
            elif record_frequency !=-1:
                self.insert_step(sim_id,i,False)
        " Write the results to the databse "
        result = append_dict(result,**{'end_entropy':self.Sim.Domain.Map.entropy(),
                                     'entropy_vec': H, 'time_vec':t,
                                     'foodcount':self.Sim.foodcount,
                                     'returncount':self.Sim.nestcount,
                                     'image_path':path+dirname,
                                     'sim_id': sim_id})
        self.insert_results(result)
        target_folder = path+dirname+'maps'
        self.save_arrays(filepath=target_folder,array_dict=Map_Dict)
        return result



    def visualize_results(self, H='', t=[], path = ''):
        P = Plotter(self.Sim.Domain.Map)
        P.draw_stigmergy(self.Sim.Domain.Map.map)
        scat_nest = circle_scatter(self.Sim.Domain.nest_location.vec, self.Sim.Domain.nest_radius)
        scat_food = circle_scatter(self.Sim.Domain.food_location.vec, self.Sim.Domain.food_radius)
        P.draw_scatter(x = scat_nest[:,0],y=scat_nest[:,1],name='nest')
        P.draw_scatter(x = scat_food[:,0],y=scat_food[:,1],name='food')
        if type(H) is not str():
            P.draw_entropy(H=H,t=t)
        if path:
            P.save(path+'final_lowres.eps',dpi=10)
            P.set_labels()
            P.set_subtitles()
            P.save(path+'final.eps', dpi=50)
        P.show()
        print("{} ants found food and {} returned".format(self.Sim.foodcount,
                                                          self.Sim.nestcount))


limits = [1000,500]
food = [750,250]
nest = [250,250]
ant_gain =2
noise_gain = 2#5/(180/np.pi)
n_ants = 80
pheromone_variance = 15
Q=20
drop_fun = 'exp_decay'
return_factor = 1.1

deploy_dict = {'n_agents': n_ants,
            'sigma': pheromone_variance,
            'deploy_method': 'instant',
            'sens_function':'linear',
            'deploy_location': 'nest',
            'target_pheromone_volume':0.1*(limits[0]+1)*(limits[1]+1)}

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
                    dt =1)
    H_steps = np.arange(0,1+1/15,1/15)
    store_map_interval = [0.1,0.25,0.5,0.75,1]
    S.connect_db(db_path = sys.path[0]+"/core/database/",
                 db_name = "stigmergy_database.db")
    sim_id = S.insert_new_sim()
    result = S.record_gradient_sim(n_steps = 1200,record_frequency=500,sim_id=sim_id,H_steps=H_steps,
                          path =  sys.path[0]+"/core/database/",store_map_interval = store_map_interval)
    S.close_db()

    S.visualize_results(np.array(result['entropy_vec']),
                        np.array(result['time_vec']),
                        path = result['image_path'] )

if __name__ == '__main__':
    test_SimRecorder()
