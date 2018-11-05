import sqlite3
import sys
from plugins.qry_vars import get_antcount, get_ant_table,get_sim
from domain import Domain
from visualization import StigmergyPlot
import numpy as np
from plugins.helper_functions import T_matrix

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
        self.id = id
        self.sqlqry = qry_object
        self.tbl = qry_object.select(get_ant_table.format(ant_id = id, sim_id = sim_id))
        self.step_range = [self.tbl[0][1],self.tbl[-1][1]]

        " initialize placeholders "
        self.steps = np.empty(self.step_range[1]-self.step_range[0])
        self.x_pos = self.steps.copy()
        self.y_pos = self.x_pos.copy()
        self.sens_y_left = self.steps.copy()
        self.sens_y_right = self.steps.copy()
        self.sens_x_left = self.steps.copy()
        self.sens_x_right = self.steps.copy()
        self.tetas = self.steps.copy()
        self.Qs = self.steps.copy()
        self.tbl_to_properties(self.tbl)

    def tbl_to_properties(self, tbl):
        " cast the sql cursor result in useable form "
        i = 0
        for row in tbl:
            self.steps[i] = row[2]
            self.x_pos[i] = row[3]
            self.y_pos[i] = row[4]
            self.tetas[i] = row[5]
            self.Qs[i] = row[6]
            T_left = T_matrix(row[5])


class SimPlayer:
    def __init__(self,sim_id, db_path, db_name):
        """ This class is the playback functionality to visualize a recording
            of a simulation """
        self.id = sim_id
        self.deploy_dict = {}
        self.domain_dict = {}
        self.ant_dict = {}
        self.sqlqry = SqlQry(db_name=db_name, db_path=db_path)
        self.n_agents = self.get_agentcount()
        self.actors = [Actor(i,sim_id,self.sqlqry)
                       for i in range(self.n_agents)]


    def get_agentcount(self):
        " Return the number of ants used in the simulation "
        return self.sqlqry.select(get_antcount.format(id=self.id))[0][0]


    def get_settings(self):
        " Get the settings used for the simulation "
        result_tuple = self.sqlqry.select(get_sim.format(id=self.id))[0]
        print(result_tuple)
        self.deploy_dict['sigma'] = result_tuple[10]
        self.deploy_dict['deploy_method'] = result_tuple[11]
        self.deploy_dict['deploy_location'] = result_tuple[12]
        self.deploy_dict['sens_function'] = result_tuple[13]
        self.domain_dict['size'] = eval(result_tuple[2])
        self.domain_dict['pitch'] = result_tuple[3]
        self.domain_dict['nest'] = {'location':eval(result_tuple[5]),
                                    'radius':result_tuple[6]}
        self.domain_dict['food'] = {'location':eval(result_tuple[7]),
                                    'radius': result_tuple[8]}
        self.domain_dict['start_concentration'] = result_tuple[9]
        "*** TODO: make start_concentration and target_pheromone equal ***"
        print(self.deploy_dict)
        print(self.domain_dict)



def run():
    db_path =sys.path[0]+"/database/"
    db_name = "stigmergy_database.db"
    # print(select_qry(get_antcount.format(id=15),db_name,db_path)[0][0])
    S = SimPlayer(15, db_path, db_name)
    S.get_settings()



if __name__=='__main__':
    run()
