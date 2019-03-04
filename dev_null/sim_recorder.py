import json
""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

from simulation import SimpleSim

class SimRecorder(SimpleSim):
    def __init__(self,*args,**kwargs):
        """
            ant_args: 'l', 'antenna_offset', 'v_max'
            dom_args: 'size', 'pitch', 'food', 'nest'
            sim_args: 'n_ants', 'pheromone_sigma', 'pheromone_Q', 'ant_speed'
        """
        SimpleSim.__init__(self,**kwargs['ants'])

    # def properties_getter(self):
    #     'size': self.size,
    #     'pitch':
    #     'n_ants':
    #     'ant_sigma':
    #     'ant_speed':
    #     'food':
    #     'nest':

        print(json.dumps(ants_args, sort_keys=True,
                   indent=2, separators=(',', ': ')))

    def print_props(self, arg = []):
        if arg:
            print(['l', 'antenna_offset','v_max','v'])
        print(self.Ants[0].properties_getter())


def check():
    ants = {'n_ants' : 50, 'ant_sigma' : 25, 'ant_speed' :10,'size':[1000,1000]}
    dom = {'x':[1000,1000]}
    S = SimRecorder(ants = ants,dom = dom)
    S.print_props()


if __name__ == '__main__':
    check()
