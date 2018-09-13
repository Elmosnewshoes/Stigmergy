import numpy as np
import time
import matplotlib.mlab as mlab
from map import MeshMap
from small_functions import gaussian, roundPartial

class AntDomain():
    """  =================================
        The playground of the simulation
        =================================="""

    def __init__(self, size = [10.,10.], pitch=0.1, local_size = 10 ):
        """  =================================
            Initialize the class
            =================================="""

        self.Map = MeshMap(dim = size, resolution = pitch, base = [0,0])

        self.update_time = 0
        self.surf_time = 0

        # Height and Width in pixels
        self.H, self.W = ((np.array(size)+pitch)/pitch).round().astype(int)

        # initialize empty map for temporary updates
        self.temp_map = self.Map.map

        # for local update
        # self.local_coords = np.arange(-round(local_size/2*pitch,2),round(local_size/2*pitch,2)+pitch,pitch)
        # self.localX, self.localY = np.meshgrid(self.local_coords, self.local_coords)
        # self.local_gaussian =  mlab.bivariate_normal(self.localX,self.localY, 0.1, 0.1, 0,0)



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
        self.Map.map = np.add(self.temp_map,self.Map.map)
        self.temp_map =  np.zeros(self.X.shape)

    # def local_add(self, loc = [2.5,3], Q = 1):
    #     rng_x = np.asarray(self.local_coords/self.pitch + loc[0]/self.pitch,dtype=int)
    #     rng_y = np.asarray(self.local_coords/self.pitch + loc[1]/self.pitch,dtype=int)
    #     print(self.X[0][rng_x])
    #     print(self.Y[rng_y][0])
    #     print(self.temp_map[:][rng_y])

    def add_pheromone(self, loc=[0,0], Q = 1., sigma = 0.5):
        """  =================================
            Add some pheromone at a location to the temporary pheromone map
            =================================="""

        tic = time.time()

        # snap x and y coordinates to grid
        x = roundPartial(loc[0],self.Map.pitch)
        y = roundPartial(loc[1],self.Map.pitch)

        """ add the pheromone """
        self.temp_map += Q*mlab.bivariate_normal(self.Map.X,self.Map.Y, sigma, sigma, x,y)
        self.update_time = time.time()-tic

    def get_pheromone_level(self, probe_point):
        """  =================================
            Return the pheromone level based on map position
            =================================="""
        x = int(round(roundPartial(probe_point[0],self.Map.pitch)/self.Map.pitch))
        y = int(round(roundPartial(probe_point[1],self.Map.pitch)/self.Map.pitch))
        # print(x,y)
        return self.pheromone_map[y,x]


def run():
    # do something to test the class
    D = AntDomain(size=[1000,1000], pitch = 1)
    print(D.Map.map.shape)
    tic = time.time()
    D.add_pheromone([1,1], Q = 1, sigma = 0.1)
    print("Added pheromone in {:.4f} msecs".format(np.dot(time.time()-tic,1e3)))
    tic2 = time.time()
    D.update_pheromone()
    # print("Updated map in {:.4f} msecs".format(np.dot(time.time()-tic2,1e3)))
    # tic3 = time.time()
    # L = D.get_pheromone_level((1,1))
    # print("Fetched pheromone in {:.4f} msecs".format(np.dot(time.time()-tic3,1e3)))
    # tic4 = time.time()
    # D.evaporate(xsi = 0.75)
    # print("Evaporate update in  in {:.4f} msecs".format(np.dot(time.time()-tic4,1e3)))
    # # print(D.get_pheromone_level((1,1)))
    # print("Total time: {:.4f} msecs".format(np.dot(time.time()-tic,1e3)))
    # print(D.local_add())

if __name__=='__main__':
    run()
