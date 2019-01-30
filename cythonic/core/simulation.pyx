# distutils: language = c++

from cythonic.core.visualization import StigmergyPlot

cdef class live_sim(Sim):
    " parent class Sim does not have the __cinit__(self,....) constructor "
    def __init__(self,queen_args, domain_args, sim_args):
        " initialize the parent class "
        super(live_sim,self).__init__(queen_args = queen_args,domain_args=domain_args, **sim_args)


    def setup_sim(self, str deposit_style, dict deposit_dict, dict gauss_dict, unsigned int display_interval,
                    visoptions = {}):
        " prepare the simulation "
        if not visoptions:
            visoptions['colormap'] = 'blue'
            visoptions['figsize'] = (10,6)
            visoptions['shown'] = 'stigmergy'

        self.chart = StigmergyPlot(x_lim = self.domain.size.x,y_lim = self.domain.size.y,**visoptions)
        self.set_depositing(deposit_style, deposit_dict )
        self.set_gaussian(**gauss_dict)
        self.interval = display_interval


    cpdef void run_sim(self, unsigned int stride):
        " loop over all steps, display the graph at specified interval "
        cdef unsigned int i
        self.chart.show()
        for i in range(self.steps):
            self.sim_step()
            if i%self.interval == 0:
                self.chart.draw_stigmergy(self.domain.Map.map[::stride,::stride])
                self.chart.draw()
        self.chart.hold_until_close()

cdef class record_sim(Sim):
    def __init__(self, queen_args, domain_args, sim_args):
        super(record_sim,self).__init__(queen_args,domain_args,sim_args)

    cpdef void run_sim(self, unsigned int store_interval):
        " loop over all steps, store the xy locations at specified interval "
        
