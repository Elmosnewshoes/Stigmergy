""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

from simulation import SimpleSim

class SimRecorder(SimpleSim):
    def __init__(self,*args,**kwargs):
        SimpleSim.__init__(self,**kwargs)



def check():
    S = SimRecorder(**{'n_ants' : 50, 'ant_sigma' : 25, 'ant_speed' :10,'size':[1000,1000]})


if __name__ == '__main__':
    check()
