import sqlite3
import sys
from core.plugins.qry_vars import get_antcount, get_ant_table,get_sim, get_latest_id
from core.domain import Domain
from core.visualization import StigmergyPlot
import numpy as np
from core.plugins.helper_functions import T_matrix, lin_fun, circle_scatter
from core.plugins.helper_classes import point

def select_qry(qry,db_name, db_path):
    db = sqlite3.connect(db_path+db_name)
    cursor = db.cursor()
    try:
        cursor.execute(qry)
    except Exception as error:
        db.close()
        raise error
    result = cursor.fetchall()
    db.close()
    if len(result) == 0:
        raise AssertionError("Zero (0) rows returned: ", qry)
    return result

class SqlQry:
    def __init__(self, db_name,db_path):
        self.db = sqlite3.connect(db_path+db_name)

    def select(self,qry):
        cursor = self.db.cursor()
        try:
            cursor.execute(qry)
        except Exception as error:
            self.db.close()
            raise error
        result = cursor.fetchall()

        if len(result) == 0:
            raise AssertionError("Zero (0) rows returned: ", qry)
        return result

    def close(self):
        self.db.close()


class Actor:
    def __init__(self,id,sim_id,qry_object,speed=0,l=0,antenna_offset=0):
        self.sqlqry = qry_object
        self.id = id
        self.tbl = qry_object.select(get_ant_table.format(ant_id = id, sim_id = sim_id))
        self.step_range = [self.tbl[0][1],self.tbl[-1][1]]

        " initialize placeholders "
        self.step_nr = np.empty(self.steps)
        self.pos_list = []
        self.sens_left_list = []
        self.sens_right_list = []
        self.tetas = self.step_nr.copy()
        self.Qs = self.step_nr.copy()
        self.tbl_to_properties()
        self.iter = -1 #keep track of the step

    def next(self):
        self.iter+=1

    @property
    def pos(self):
        try:
            return self.pos_list[self.iter]
        except Exception as error:
            print("iteration ",self.iter)
            raise error

    @property
    def Q(self):
        return self.Qs[self.iter]

    @property
    def steps(self):
        return int(self.step_range[1]-self.step_range[0]+1)

    def tbl_to_properties(self):
        " cast the sql cursor result in useable form "
        i = 0
        for row in self.tbl:
            self.step_nr[i] = row[1]
            self.pos_list.append(point(row[3],row[4]))
            self.tetas[i] = row[5]
            self.Qs[i] = row[6]
            T_left = T_matrix(row[5])
            i+=1


class SimPlayer:
    def __init__(self,sim_id, db_path, db_name):
        """ This class is the playback functionality to visualize a recording
            of a simulation """
        self.deploy_dict = {}
        self.domain_dict = {}
        self.ant_dict = {}
        self.sqlqry = SqlQry(db_name=db_name, db_path=db_path)
        if sim_id =='latest':
            self.id = self.sqlqry.select(qry=get_latest_id)[0][0]
            print(f"fetching sim {self.id}")
        else:
            self.id = sim_id
        self.n_agents = self.get_agentcount()
        self.actors = [Actor(i,self.id,self.sqlqry)
                       for i in range(self.n_agents)]

    def xy(self,n):
        xy = np.zeros((self.n_agents,2))
        i = 0
        for ant in self.actors:
            xy[i] = ant.pos.vec
            i+=1
        return xy[:,0], xy[:,1]


    def get_agentcount(self):
        " Return the number of ants used in the simulation "
        return self.sqlqry.select(get_antcount.format(id=self.id))[0][0]


    def get_settings(self):
        " Get the settings used for the simulation "
        result_tuple = self.sqlqry.select(get_sim.format(id=self.id))[0]
        self.deploy_dict['target_pheromone_volume'] = result_tuple[9]
        self.deploy_dict['sigma'] = result_tuple[10]
        self.domain_dict['size'] = eval(result_tuple[2])
        self.domain_dict['pitch'] = result_tuple[3]
        self.domain_dict['nest'] = {'location':eval(result_tuple[5]),
                                    'radius':result_tuple[6]}
        self.domain_dict['food'] = {'location':eval(result_tuple[7]),
                                    'radius': result_tuple[8]}
        self.ant_dict['start_speed'] = result_tuple[14]
        self.ant_dict['antenna_offset'] =result_tuple[15]
        self.ant_dict['l'] = result_tuple[16]

    def deploy_domain(self):
        self.Domain = Domain(**self.domain_dict)

    def init_sim(self,sigma,target_pheromone_volume):
        self.Domain.Gaussian = self.Domain.init_gaussian(sigma)
        self.Domain.set_target_pheromone(target_pheromone_volume)
        self.Domain.evaporate()
        # self.Domain.update_pheromone()

    def prep_visualization(self):
        self.P = StigmergyPlot(self.Domain.Map, n=10)
        self.P.draw_stigmergy(self.Domain.Map.map)
        scat_nest = circle_scatter(self.Domain.nest_location.vec, self.Domain.nest_radius)
        scat_food = circle_scatter(self.Domain.food_location.vec, self.Domain.food_radius)
        self.P.draw_scatter(x = scat_nest[:,0],y=scat_nest[:,1],
                            marker = '.',name='nest',s=20)
        self.P.draw_scatter(x = scat_food[:,0],y=scat_food[:,1],
                            marker = '.',name='food',s=20)


    def run_sim(self, visualization = False):
        " actual replay part "
        n = self.actors[0].steps
        for i in range(n):
            for ant in self.actors:
                ant.next()
                self.Domain.local_add_pheromone(target_pos= ant.pos, Q = ant.Q)
            self.Domain.evaporate()
            if visualization:
                X,Y = self.xy(n)
                self.P.draw_scatter(X,Y,name='ant')
                self.P.draw_stigmergy(self.Domain.Map.map)
                self.P.draw()
        self.P.hold_until_close()



def run():
    db_path =sys.path[0]+"/core/database/"
    db_name = "stigmergy_database.db"
    S = SimPlayer('latest', db_path, db_name)
    S.get_settings()
    S.deploy_domain()
    S.init_sim(**S.deploy_dict)
    S.prep_visualization()
    S.run_sim(visualization = True)



if __name__=='__main__':
    run()
