import json
from cythonic.plugins import queries
import numpy as np

cdef class sim_recorder(Sim):
    def __init__(self,queen_args, domain_args, sim_args):
        """ Need to store the dicts for inserting into database """
        self.queen_dict = queen_args
        self.sim_dict = sim_args
        self.domain_dict = domain_args
        self.ant_dict=queen_args['ant_dict']
        super(sim_recorder,self).__init__(queen_args = queen_args, domain_args = domain_args, **sim_args)

    def init_connection(self,str path, str dbname):
        self.db = db_controller(path,dbname)

    def setup_sim(self, dict deposit_dict, dict gauss_dict, unsigned int upload_interval):
        " prepare the simulation "
        self.update_interval = upload_interval
        self.set_depositing(self.ant_dict['deposit_fun'], deposit_dict )
        self.set_gaussian(**gauss_dict)
        self.id = self.db.new_sim_id()
        self.push_settings(deposit_dict, gauss_dict)
        self.flush_resultset() # initialize the insert state query

    def push_settings(self, dict deposit_dict, dict gauss_dict):
        """ INSERT the simulation settings into the database prior to experiment """
        # manipulation, convert nested dict to string for database
        cdef dict sim_dict = self.sim_dict.copy()
        sim_dict['deploy_timing_args'] = json.dumps(self.sim_dict['deploy_timing_args']).replace("'","''")

        queries_list =(
            queries.insert_ant(self.id, **self.ant_dict),
            queries.insert_queen(self.id,**self.queen_dict),
            queries.insert_domain(self.id,**self.domain_dict),
            queries.insert_gauss(self.id,**gauss_dict),
            queries.insert_deposit(self.id,**deposit_dict),
            queries.insert_sens(self.id,**self.ant_dict['sens_dict']),
            queries.sim_settings(self.id,**sim_dict), # use the local manipulated copy of sim_dict
                    )
        for qry in queries_list:
            self.db.execute(qry)

    cdef void flush_resultset(self,):
        " prepare for a new batch of settings "
#         self.pending_qry = queries.insert_stepupdates()
        self.qry_args = []
        self.pending_qry = "INSERT INTO STEP (SIM_ID, STEP_NR, ANT_ID, X, Y, THETA, Q) VALUES (?,?,?,?,?,?,?)"

    cdef void extract_antstate(self, unsigned int step):
        " make a copy of the vital ant state elements and store "
        cdef unsigned int i
        for i in range(self.queen.count_active):
            " push the state to a list "
            self.qry_args.append((self.id, step, self.queen.state_list[i].id, self.queen.state_list[i].pos.x,
                                  self.queen.state_list[i].pos.y, self.queen.state_list[i].theta,
                                  self.queen.drop_quantity[i]))

    cdef void record_step(self, unsigned int stepnr):
        " record the state at each step "
        self.extract_antstate(stepnr) #append query with current ant_state
        if stepnr>0 and (stepnr==self.steps-1 or stepnr%self.update_interval ==0):
            # check if results must be pushed to the database
            self.db.executemany(self.pending_qry, self.qry_args)
            self.flush_resultset() # start with a fresh query string


    cdef dict run_sim(self, bint record):
        " run the simulation "
        cdef unsigned int i #stepcounter
        cdef unsigned int action_counter = 0 #count all ant actions
        cdef double start_entropy = self.domain.entropy()
        cdef double end_entropy = 0 #placeholder for resulting entropy
        cdef unsigned int stepupdates = 0 #counter for storing the result
        cdef unsigned int[:] k_vec = np.arange(0,self.steps+1, <unsigned int>int(np.ceil(self.steps/100)), dtype = np.uint32)
        k_vec[len(k_vec)-1] = self.steps #make sure the last performance sample is taken at the last step
        cdef list entropy_vec = [], nestcount_vec = []
        if record:
            self.db.execute(f"UPDATE sim SET RECORDING = 'TRUE' WHERE ID = {self.id}")
        self.db.execute(queries.update_sim(self.id, status = 'STARTED'))

        # === loop ===
        for i in range(self.steps+1):
            self.sim_step() # do the stepping
            if record:
                # do the recording
                action_counter +=self.queen.count_active
                if i == k_vec[stepupdates]:
                    # this iteration the result vector is appended
                    entropy_vec.append(round(self.domain.entropy(),3))
                    nestcount_vec.append(self.nestcount)
                    stepupdates+=1 # increase the vector index

                self.record_step(i)
        # === end loop ===

        # store results:
        end_entropy = self.domain.entropy()

        result = {'sim_id': self.id,'foodcount': self.foodcount, 'nestcount': self.nestcount,
               'entropy_vec': entropy_vec, 'start_entropy': round(start_entropy,3), 'end_entropy': round(end_entropy,3),
                'scorecard':nestcount_vec, 'step_vec':np.asarray(k_vec).tolist()}
        self.db.execute(queries.insert_results(**result))
        if record:
            self.db.execute(queries.update_sim(self.id, status = 'FINISHED', steps = action_counter))
        else:
            self.db.execute(queries.update_sim(self.id, status = 'FINISHED'))
        return result
