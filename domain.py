import numpy as np
import time
import matplotlib.mlab as mlab
from map import MeshMap
from small_functions import roundPartial

" Volume of the gaussian is not on to par yet"

class AntDomain():
    """  =================================
        The playground of the simulation
        =================================="""

    def __init__(self, size = [10.,10.], pitch=0.1):
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

        # get a gaussian map (initialize with zeros)
        self.Gaussian = MeshMap(dim = np.dot(size,1e-1), resolution=pitch)

    def set_gaussian(self,sigma):
        self.Gaussian.init_map(map_type='gaussian',covariance = sigma)

    def evaporate(self, xsi):
        """ ========================
            perform an evaporation step
            on the pheromone map with evap. constant xsi
            (since lambda is system name)
            ========================"""
        self.Map.map = np.multiply(self.Map.map,xsi)

    def update_pheromone(self,):
        """ =========================
            Here the contribution of the temp map is added to
            the global pheromone map
            ========================="""
        self.Map.map = np.add(self.temp_map,self.Map.map)
        self.temp_map =  np.zeros(self.Map.X.shape)

    def local_add_pheromone(self,loc=[0,0], Q=1.):
        """  =================================
            Add some pheromone at a location to the temporary pheromone map,
            based on stored preshaped normalized gaussian
            =================================="""
        # get grid coordinates
        x,y = loc

        span_x1, span_x2 = self.Gaussian.map.shape
        X_range, X_prop = self.Map.span(base = x, axis = 'X', span = int((span_x1-1)/2))
        Y_range, Y_prop = self.Map.span(base = y, axis = 'Y', span = int((span_x2-1)/2))


        # pointer to a temp map that can be sliced and diced
        tmp_gauss = self.Gaussian.map

        # check if guassian needs slicing
        if X_prop['error'] == True:
            if X_prop['limit'] =='upper':
                tmp_gauss = tmp_gauss[:-int(X_range[0]-X_range[1]),:]
            else:
                tmp_gauss = tmp_gauss[-int(X_range[1]-X_range[0]):,:]
        if Y_prop['error'] == True:
            if Y_prop['limit'] == 'upper':
                tmp_gauss = tmp_gauss[:,:-int(Y_range[0]-Y_range[1])]
            else:
                tmp_gauss = tmp_gauss[:,-int(Y_range[1]-Y_range[0]):]

        # finally, insert the gaussian in the temp_map
        self.temp_map[X_range[0]:X_range[1],
                      Y_range[0]:Y_range[1]] = np.dot(Q,tmp_gauss)



    def add_pheromone(self, loc=[0,0], Q = 1., sigma = 0.5):
        """  =================================
            Add some pheromone at a location to the temporary pheromone map
            =================================="""
        tic = time.time()
        x,y = loc

        """ add the pheromone """
        self.temp_map += Q*mlab.bivariate_normal(self.Map.X,self.Map.Y, sigma, sigma, x,y)
        self.update_time = time.time()-tic

    def get_pheromone_level(self, probe_point):
        """  =================================
            Return the pheromone level based on map position in mm
            =================================="""
        x1,x2 = self.Map.coord2grid(probe_point)
        return self.Map.map[x1,x2]

def run():
    # do something to test the class
    D = AntDomain(size=[1000,1000], pitch = 5)
    print(D.Map.map.shape)
    tic = time.time()
    D.add_pheromone([1,1], Q = 1, sigma = 0.1)
    print("Added pheromone in {:.4f} msecs".format(np.dot(time.time()-tic,1e3)))
    tic2 = time.time()
    D.update_pheromone()
    print("Updated map in {:.4f} msecs".format(np.dot(time.time()-tic2,1e3)))
    tic3 = time.time()
    L = D.get_pheromone_level([1,1])
    print("Fetched pheromone in {:.4f} msecs".format(np.dot(time.time()-tic3,1e3)))
    print(L)
    print(D.Map.map.sum()*D.Map.pitch*D.Map.pitch)
    tic4 = time.time()
    D.evaporate(xsi = 0.75)
    print("Evaporate update in  in {:.4f} msecs".format(np.dot(time.time()-tic4,1e3)))
    print("Total time: {:.4f} msecs".format(np.dot(time.time()-tic,1e3)))
    # print(D.local_add())

    print(D.Gaussian.map.shape)
    tic = time.time()
    D.local_add_pheromone([150,150])
    print("Local add took {:.4f} msec".format(np.dot(time.time()-tic,1e3)))
if __name__=='__main__':
    run()
