import json
from cythonic.plugins import queries

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

    def setup_sim(self, str deposit_style, dict deposit_dict, dict gauss_dict, unsigned int upload_interval):
        " prepare the simulation "
        self.update_interval = upload_interval
        self.set_depositing(deposit_style, deposit_dict )
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
        if i>0 and (i==self.steps-1 or i%self.update_interval ==0):
            # check if results must be pushed to the database
            self.db.executemany(self.pending_qry, self.qry_args)
            self.flush_resultset() # start with a fresh query string


    cdef dict run_sim(self, bint record):
        " run the simulation "
        cdef unsigned int i #stepcounter
        cdef double start_entropy = self.domain.entropy()
        cdef double end_entropy = 0
        cdef unsigned int stepupdates = 0
        cdef k_vec = np.arange(0,self.steps+1, int(np.ceil(self.steps/12)))
        k_vec[len(k_vec)-1] = self.steps+1
        if record:
            self.db.execute(f"UPDATE sim SET RECORDING = 'TRUE' WHERE ID = {self.id}")
        self.db.execute(queries.update_sim(self.id, status = 'STARTED'))

        # === loop ===
        for i in range(self.steps+1):
            self.sim_step() # do the stepping
            if record:
                # do the recording
                self.record_step(i)

            # if record:
            #     # check if the recording flag is true: store the ant state
            #     self.extract_antstate(i)
            #     stepupdates+=self.queen.count_active # keep track of total steps performed
            #     if i>0 and (i == self.steps-1 or i%self.update_interval == 0):
            #         # check if results are to be pushed to the database
            #         self.db.executemany(self.pending_qry,self.qry_args)
            #         self.flush_resultset() # start with a fresh query
        # === end loop ===

        result = {'sim_id': self.id,'foodcount': self.foodcount, 'nestcount': self.nestcount,
               'entropy_vec': 'NULL', 'start_entropy': 'NULL', 'end_entropy': 'NULL'}
        self.db.execute(queries.insert_results(**result))
        self.db.execute(queries.update_sim(self.id, status = 'FINISHED'))
        return result
