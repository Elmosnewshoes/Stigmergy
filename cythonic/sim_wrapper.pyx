from cythonic.core.sim_recorder cimport sim_recorder
from time import time
cimport cython

@cython.wraparound(True)
def db_path():
    " return the full path to the database "
    import inspect
    from cythonic.database.__init__ import dummy
    path = inspect.getabsfile(dummy)
    return '/'.join(path.split('/')[:-1])+'/'

cdef class recorder(sim_recorder):
    def __init__(self,queen_args, domain_args, sim_args):
        """ wrapper class constructor """
        # initialize the parent class
        super(recorder,self).__init__(queen_args, domain_args, sim_args)

    def pysetup_sim(self, str deposit_style, dict deposit_dict, dict gauss_dict, unsigned int upload_interval):
        """ wrap setup_sim and make available to python """
        self.setup_sim(deposit_style = deposit_style, deposit_dict = deposit_dict, gauss_dict = gauss_dict, upload_interval =500,)

    def pyrun_sim(self, bint record):
        self.run_sim(record = record)

    def time_full_sim(self, bint record, str deposit_style, dict deposit_dict, dict gauss_dict, unsigned int upload_interval = 0):
        cdef double toc, tic = time()
        self.init_connection(db_path(),'stigmergy.db')
        self.setup_sim(deposit_style, deposit_dict, gauss_dict, upload_interval,)
        result = self.run_sim(record)
        self.db.close()

        toc = time()
        print(f" \n Simulation with ID: {self.id}")
        print(f" \n It took a whopping {(toc-tic)*1000} msec \n")
        return result
