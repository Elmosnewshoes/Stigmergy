from cythonic.core.sim_recorder cimport sim_recorder
from cythonic.core.sim_controller cimport Sim
from time import time
cimport cython
from cythonic.plugins.db_path import db_path
from cythonic.plugins.queries import set_activator

cdef class recorder(sim_recorder):
    def __init__(self,queen_args, domain_args, sim_args):
        """ wrapper class constructor """
        # initialize the parent class
        super(recorder,self).__init__(queen_args, domain_args, sim_args)

    def pysetup_sim(self, str deposit_style, dict deposit_dict, dict gauss_dict, unsigned int upload_interval):
        """ wrap setup_sim and make available to python """
        self.setup_sim(deposit_style = deposit_style, deposit_dict = deposit_dict, gauss_dict = gauss_dict, upload_interval =500,)

    def pyrun_sim(self, bint record, str initiator):
        self.run_sim(record = record, initiator = initiator)

    def time_full_sim(self, bint record, dict deposit_dict,
                        dict gauss_dict, unsigned int upload_interval = 0,
                         initiator = ''):
        cdef double toc, tic = time()
        self.init_connection(db_path(),'stigmergy.db')
        self.setup_sim( deposit_dict, gauss_dict, upload_interval,)
        result = self.run_sim(record, initiator = initiator )
        self.db.close()

        toc = time()
        print(f" \n Simulation with ID: {self.id}")
        print(f" \n It took a whopping {(toc-tic)*1000} msec \n")
        return result
cdef class controller(Sim):
    def __init__(self,queen_args,domain_args,sim_args):
        "wrap constructor "
        super().__init__(queen_args, domain_args,**sim_args)
    def pysetup_sim(self, str deposit_style, dict deposit_dict, dict gauss_dict):
        self.set_depositing(deposit_style, deposit_dict)
        self.set_gaussian(**gauss_dict)

    def pyrun_sim(self):
        for i in range(self.steps):
            self.sim_step()
        result = {'sim_id': self.id,'foodcount': self.foodcount, 'nestcount': self.nestcount}
        return result
