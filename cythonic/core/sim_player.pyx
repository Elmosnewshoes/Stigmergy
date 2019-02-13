from cythonic.plugins.db_controller cimport db_controller
from cythonic.plugins.db_path import db_path
from cythonic.plugins.queries import get_settings, get_steps
from cythonic.plugins.positions cimport point
cimport cython
from libc.math cimport M_PI, sin as csin, cos as ccos
import numpy as np

def extract_settings(rows, headers):
    return {headers[i]:rows[0][i] for i in range(len(headers))}

cdef double rotate_x(double l, double theta):
    "rotate by theta in radians "
    return ccos(theta)*l

cdef double rotate_y(double l, double theta):
    return csin(theta)*l

cdef double deg2rad(double theta ):
    return theta*M_PI/180

@cython.boundscheck(True)
@cython.wraparound(True)
cdef class SimPlayer:
    def __init__(self,sim_id, db_name, db_path = db_path()):
        self.db = db_controller(db_path, db_name)
        self.id = sim_id

        # d,h = self.db.return_all(get_settings(sim_id, 'sim_settings'))
        " extract settings yields a dictionary with parameter-value combinations"
        sim_settings = extract_settings(*self.db.return_all(get_settings(sim_id,'sim_settings')))
        ant_settings = extract_settings(*self.db.return_all(get_settings(sim_id,'ant_settings')))
        gauss_settings = extract_settings(*self.db.return_all(get_settings(sim_id,'gauss_settings')))

        self.evap_rate = sim_settings['evap_rate']
        self.n_agents = sim_settings['n_agents']
        self.steps = sim_settings['steps']
        self.ant_size = ant_settings['l']
        self.sens_offset = ant_settings['sens_offset']
        self.positions = np.zeros([self.n_agents,2],dtype = np.float_)
        self.headings = np.zeros(self.n_agents, dtype =np.float_)
        self.lefts = np.zeros([self.n_agents,2],dtype = np.float_)
        self.rights = np.zeros([self.n_agents,2],dtype = np.float_)


        " initialize the objects "
        self.init_domain()
        self.init_gaussian(gauss_settings)
        self.count_active = 0

    def init_domain(self,):
        " extract the query into useable initialization parameters "
        domain_dict = extract_settings(*self.db.return_all(get_settings(self.id,'domain_settings')))
        del domain_dict['sim_id'] # remove sim_id from dict
        cdef dict dom_dict = {}
        for key, value in domain_dict.items():
            if type(value) is str:
                dom_dict[key] = eval(value)
            else:
                dom_dict[key] = value
        self.domain = Domain(**dom_dict)

    def init_gaussian(self, gauss_dict):
        del gauss_dict['sim_id'] # remove sim_id from dict
        self.domain.init_gaussian(gauss_dict['covariance'], gauss_dict['significancy'])


    def get_steps(self ):
        " get dataframe from qry "
        qry = get_steps(self.id)
        self.ant_steps = self.db.get_df(qry)

    def get_results(self,):
        results = extract_settings(*self.db.return_all(get_settings(self.id,'results')))
        " check if step_vec, scorecard and entropy_vec are not NULL, then store as object attribute "
        if results['step_vec']:
            self.steplist = np.asarray(eval(results['step_vec']),dtype=np.uint32)
            if not results['scorecard']:
                " no results in query "
                self.nestcount = np.zeros(self.steplist.shape[0], dtype = np.uint32)
            else:
                self.nestcount = np.asarray(eval(results['scorecard']),dtype = np.uint32)
            if not results['entropy_vec']:
                " no results in query "
                self.entropy = np.zeros(self.steplist.shape[0], dtype = np.float_)
            else:
                self.entropy = np.asarray(eval(results['entropy_vec']),dtype = np.float_)

    cpdef void next(self,):
        self.step(self.cur_step)
        self.cur_step+=1

    cpdef void renew(self,):
        self.cur_step = 0
        self.domain.reset()


    cdef void step(self, unsigned int stepnr):
        " do a step "
        cdef double x,y, theta, q
        cdef point pos
        cdef unsigned int i = 0 # iterator for positions, headings, lefts and rights
        for row in self.ant_steps[self.ant_steps['STEP_NR']== stepnr].itertuples(index = False):
            pos.x = row.X
            pos.y = row.Y
            theta = row.THETA
            q = row.Q
            self.positions[i,0] = pos.x
            self.positions[i,1] = pos.y
            self.headings[i] = theta
            self.lefts[i,0] = pos.x+rotate_x(l = self.ant_size,theta = deg2rad(theta+self.sens_offset))
            self.lefts[i,1] = pos.y+rotate_y(l = self.ant_size,theta = deg2rad(theta+self.sens_offset))
            self.rights[i,0] = pos.x+rotate_x(l = self.ant_size,theta = deg2rad(theta-self.sens_offset))
            self.rights[i,1] = pos.y+rotate_y(l = self.ant_size,theta = deg2rad(theta-self.sens_offset))
            self.domain.add_pheromone(p = &pos, Q = &q)

            i+=1
        self.domain.evaporate(tau = &self.evap_rate)
        self.count_active = i # keep track of how many ants are stepping each iteration

    def run_until(self, lim):
        " return the map at a certain stage "
        while self.cur_step < lim:
            self.next()
        return self.map

    @property
    def H(self ):
        " return result entropy vector from k==0 up to and including K==cur_step "
        return np.asarray(self.entropy)[np.asarray(self.steplist)<=self.cur_step]
    @property
    def K(self ):
        " return result step vector from k==0 up to and including K==cur_step "
        return np.asarray(self.steplist)[np.asarray(self.steplist)<=self.cur_step]
    @property
    def score(self ):
        return np.asarray(self.nestcount)[np.asarray(self.steplist)<=self.cur_step]

    @property
    def H_vec(self):
        return np.asarray(self.entropy)
    @property
    def K_vec(self):
        return np.asarray(self.steplist)
    @property
    def score_vec(self):
        return np.asarray(self.nestcount)

    @property
    def pos_x(self):
        return np.asarray(self.positions[:self.count_active,0])
    @property
    def pos_y(self):
        return np.asarray(self.positions[:self.count_active,1])
    @property
    def left_x(self):
        return np.asarray(self.lefts[:self.count_active,0])
    @property
    def left_y(self):
        return np.asarray(self.lefts[:self.count_active,1])
    @property
    def right_x(self):
        return np.asarray(self.rights[:self.count_active,0])
    @property
    def right_y(self):
        return np.asarray(self.rights[:self.count_active,1])
    @property
    def heading(self):
        return np.asarray(self.headings[:self.count_active])
    @property
    def map(self):
        return np.asarray(self.domain.Map.map)
    @property
    def xlim(self):
        return self.domain.size.x
    @property
    def ylim(self):
        return self.domain.size.y
