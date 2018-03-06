import numpy as np
import time
import matplotlib.mlab as mlab

def roundPartial (value, resolution):
    return round (value / resolution) * resolution

def gaussian(X,Y, mu, sig):
    """ ==============================
        Redundant, mlab.bivariate_normal does the same but faster
        calculate the value of a 2D NORMALIZED gaussian function
        e.g.: Volume of f(x,y)==1
        ============================== """
    A = sig*sig*2*np.pi
    G = np.exp(-np.add(np.power(X-mu[0],2)/(2*np.power(sig,2)),np.power(Y-mu[1],2)/(2*np.power(sig,2))))
    return G/A



class AntDomain():
    """  =================================
        The playground of the simulation
        =================================="""

    def __init__(self, size = (10.,10.), pitch=0.1 ):
        """  =================================
            Initialize the class
            =================================="""

        self.update_time = 0
        self.surf_time = 0

        # pixels per mm
        self.pitch = pitch

        # Height and Width in pixels
        self.H, self.W = ((np.array(size)+pitch)/pitch).round().astype(int)

        # pixel coordinates
        self.xx = np.arange(0,size[1]+pitch,self.pitch)
        self.yy = np.arange(0,size[0]+pitch,self.pitch)
        self.X, self.Y = np.meshgrid(self.xx,self.yy)

        # initialize empty pheromone map
        self.pheromone_map = np.zeros(self.X.shape)
        self.temp_map = np.zeros(self.X.shape)

    def evaporate(self, xsi):
        """ ========================
            perform an evaporation step
            on the pheromone map with evap. constant xsi
            (since lambda is system name)
            ========================"""
        self.pheromone_map = np.multiply(self.pheromone_map,xsi)

    def update_pheromone(self,):
        """ =========================
            Here the contribution of the temp map is added to
            the global pheromone map
            ========================="""
        self.pheromone_map= np.add(self.temp_map,self.pheromone_map)
        self.temp_map =  np.zeros(self.X.shape)

    def add_pheromone(self, loc=(0,0), Q = 1., sigma = 0.5):
        """  =================================
            Add some pheromone at a location to the temporary pheromone map
            =================================="""

        tic = time.time()

        # snap x and y coordinates to grid
        x = roundPartial(loc[0],self.pitch)
        y = roundPartial(loc[1],self.pitch)

        """ add the pheromone """
        # self.pheromone_map = np.add(self.pheromone_map,mlab.bivariate_normal(self.X,self.Y, sigma, sigma, x,y))
        self.temp_map += Q*mlab.bivariate_normal(self.X,self.Y, sigma, sigma, x,y)
        self.update_time = time.time()-tic

    def get_pheromone_level(self, probe_point):
        """  =================================
            Return the pheromone level based on map position
            =================================="""
        x = int(round(roundPartial(probe_point[0],self.pitch)/self.pitch))
        y = int(round(roundPartial(probe_point[1],self.pitch)/self.pitch))
        # print(x,y)
        return self.pheromone_map[y,x]


def run():
    # do something to test the class
    D = AntDomain(size=(100,100), pitch = 0.1)
    D.add_pheromone((1,1), Q = 1, sigma = 1)
    print(D.get_pheromone_level((1,1)))
    D.update_pheromone()
    print(D.get_pheromone_level((1,1)))
    D.evaporate(xsi = 0.75)
    print(D.get_pheromone_level((1,1)))


if __name__=='__main__':
    run()
