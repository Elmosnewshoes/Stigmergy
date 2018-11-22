import sys,time

import numpy as np
import matplotlib.pyplot as plt



def gaussian(x, mu, sig):
    """ ==============================
        calculate the value of a 1D NORMALIZED gaussian function
        e.g.: integral of f(x)==1
        ============================== """
    return np.sqrt( 1/(2 * np.power(sig, 2.))/np.pi)*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

class domain:
    """  =================================
        The playground of the simulation
        =================================="""

    def __init__(self, h, w, res=1., sigma = 0.1):
        """  =================================
            Initialize the class
            =================================="""

        self.unit = "mm" # scale
        self.grid_resolution =  res # pixels per unit

        self.grid_height = int(round(h/self.grid_resolution,0))+1
        self.grid_width = int(round(w/self.grid_resolution,0))+1

        self.pheromone_sig = sigma

        self.pheromone_map = np.zeros((self.grid_height, self.grid_width))
        self.surface_plot = self.pheromone_map
        self.X, self.Y = np.meshgrid(np.linspace(0,self.grid_height-1,self.grid_height), np.linspace(0,self.grid_width-1,self.grid_width))

    def addPheromone(self, xy, amount):
        """ =================================
            Add amount of pheromone to the pheromone map at all xy locations
            ================================="""

        for xy,p in zip(xy,amount):
            x, y = np.around(np.array(xy)/self.grid_resolution).astype(int) # mm to grid location
            self.pheromone_map[x,y] += p

    def pheromoneLevel(self,xy, n = 10):
        """ =================================
            calculate the pheromone level based on xy coordinate in mm
            first, calculate the radial distance to all points
            second, take top 10 closest points
            finally, sum the pheromone levels
            ================================="""
        Q = 0 # pheromone level, to be returned at the end
        # x,y = xy # the coordinates
        # yv, xv = np.meshgrid(np.linspace(0,self.grid_height-1,self.grid_height), np.linspace(0,self.grid_width-1,self.grid_width))
        mesh_vec = np.dstack((np.asarray(self.X).reshape(-1), np.asarray(self.Y).reshape(-1)))

        # difference between grid points and xy
        diff = mesh_vec - xy

        # distance between grid points and xy (pythagoras)
        R = np.sqrt(np.power(diff[0][:,0],2)+np.power(diff[0][:,1],2))

        # x = X_sort[:,0], y = X_sort[:,1], R = X_sort[:,2]
        R_sort = np.array(sorted(np.dstack((mesh_vec,R)).tolist()[0], key=lambda x : x[2]))

        # sum the pheromone level at the n closest points
        print(self.pheromone_map)
        for ii in range(min(n,self.pheromone_map.size)):
            P = self.pheromone_map[int(R_sort[ii,0]),int(R_sort[ii,1])]# pheromone on the point
            Q += gaussian(R_sort[ii,2],0,self.pheromone_sig)
            print('At ({},{}), P = {}'.format(int(R_sort[ii,0]),int(R_sort[ii,1]),P))
        print(Q)

    def calcMap(self):
        """ =========================
            calculate the plotting surface
            ========================="""
        for yy in range(self.pheromone_map.shape[0]):
            for xx in range(self.pheromone_map.shape[1]):





def run():
    # dx = 0.01
    # S = 0
    # sig = 0.1
    # for x in [x*dx for x in range(int(-10/dx),int(10/dx),1)]:
    #     S+=gaussian(x,0,sig)*dx
    # print(S)
    # print(np.sqrt( 1/(2 * np.power(sig, 2.))/np.pi))

    D = domain(3,3,0.5,sigma = 0.1)
    print(D.pheromone_map)
    D.addPheromone([[1.1,1.1],[2.6,2.6]], [3,4])
    print(D.pheromone_map)
    D.pheromoneLevel((1.1,1.1),100)
    D.calcMap()

if __name__ == '__main__':
    run()
