import sys,time
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
from scipy.interpolate import RectBivariateSpline
from scipy import interpolate

# np.set_printoptions(threshold=np.nan)

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'in'
plt.ion()

def gaussian(X,Y, mu, sig):
    """ ==============================
        calculate the value of a 2D NORMALIZED gaussian function
        e.g.: Volume of f(x,y)==1
        ============================== """
    A = sig*sig*2*np.pi
    G = np.exp(-np.add(np.power(X-mu[0],2)/(2*np.power(sig,2)),np.power(Y-mu[1],2)/(2*np.power(sig,2))))
    return G/A

def roundPartial (value, resolution):
    return round (value / resolution) * resolution


class AntDomain():
    """  =================================
        The playground of the simulation
        =================================="""

    def __init__(self, size = (10.,10.), pitch=0.1 ):
        """  =================================
            Initialize the class
            =================================="""

        self.draw_time = 0
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

    def set_plot(self, colorscheme = cm.gray_r):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.surf = plt.imshow(self.pheromone_map, interpolation='bilinear', origin='lower',
                        cmap=colorscheme, extent=(0, self.W*self.pitch, 0, self.H*self.pitch))
        plt.title('simple contour plot')


    def add_pheromone(self, loc=(0,0), Q = 1., sigma = 0.5):
        """  =================================
            Add pheromone to the map at location (x,y)
            amount: Q
            varriance: sigma (assumed cov = I)
            =================================="""

        tic = time.time()

        # snap x and y coordinates to grid
        x = roundPartial(loc[0],self.pitch)
        y = roundPartial(loc[1],self.pitch)

        """ add the pheromone """
        # self.pheromone_map = np.add(self.pheromone_map,mlab.bivariate_normal(self.X,self.Y, sigma, sigma, x,y))
        self.pheromone_map += mlab.bivariate_normal(self.X,self.Y, sigma, sigma, x,y)
        self.update_time = time.time()-tic

    def plot(self, colorscheme = cm.gray_r):
        """  =================================
            Update the heatmap of the pheromone
            =================================="""
        tic = time.time()

        # new surface data
        self.fig.clf() # purge the old figure
        self.surf = plt.imshow(self.pheromone_map[0::2,0::2], interpolation='bilinear', origin='lower',
                        cmap=colorscheme, extent=(0, np.dot(self.W,self.pitch), 0, np.dot(self.H,self.pitch)))

        self.surf_time = time.time()-tic
        # update the canvas
        self.fig.canvas.draw()

        self.draw_time = time.time()-tic

    def hold_until_close(self):
        # keep the plotting window open until manually closed
        plt.show(block = True)

    def get_pheromone_level(self, probe_point):
        """  =================================
            Return the pheromone level based on map position
            =================================="""
        x = int(round(roundPartial(probe_point[0],self.pitch)/self.pitch))
        y = int(round(roundPartial(probe_point[1],self.pitch)/self.pitch))
        # print(x,y)
        return self.pheromone_map[y,x]


class Ant():
    """ ===========================
        The main agents/actors in the simulation
        =========================== """
    # start_pos (x,y) in mm
    # limits (x_lim, y_lim) in mm

    def __init__(self, start_pos = (1,1), seed = int(time.time()), limits = (10,10)):
        """  =================================
            Initialize the class
            ================================== """

        self.x, self.y = start_pos #in mm
        self.limits = limits

        # assign private RNG
        self.gen = np.random.RandomState(seed)

    def random_step(self, sigma = 0.1):
        """ ============================
            perform a random rand_step
            ============================ """
        # loop until a valid move
        ii = 0
        while True:
            ii+=1
            # draw a step from the RNG
            rand_step = self.gen.randn(2,1)

            # update the next position and check validity
            pos = [[self.x],[self.y]] + rand_step*sigma
            if (0<=pos[0][0]<=self.limits[0]) and (0<=pos[1][0]<=self.limits[1]):
                # we have a valid move -> update new position
                self.x = pos[0][0]
                self.y = pos[1][0]
                return((self.x,self.y))
            else:
                print('misstep {} at x = {}; y = {}'.format(ii,  pos[0][0], pos[1][0]))





def run():
    pitch = 0.5
    domain_limits = (100,100)
    D = AntDomain(size=domain_limits,pitch=pitch)
    D.set_plot()

    # # D.add_pheromone((1,1))
    # x = np.arange(0,20,2*pitch)
    # y = np.arange(0,10,pitch)


    # for ii in range(x.size):
    #     tic = time.time()
    #     D.add_pheromone((x[ii]/pitch,y[ii]/pitch), sigma = 0.25)
    #     D.plot()
        # print("Step {} took {} sec -- surf time = {} -- draw time = {} -- update_time = {}".format(ii, time.time()-tic,D.surf_time, D.draw_time,D.update_time))

    A = Ant(limits = domain_limits,seed =int(time.time()-1000), start_pos=(10,20))
    A2 = Ant(limits = domain_limits, start_pos=(50,50))
    for ii in range(100):

        tic = time.time()
        # A.random_step(sigma = 2)
        # A2.random_step(sigma =5)
        D.add_pheromone(A.random_step(sigma=2),sigma=4)
        D.add_pheromone(A2.random_step(sigma=5),sigma=4)
        print("Step {} -- Pheromone level = {}".format(ii,D.get_pheromone_level((A.x,A.y))))
        if ii%1==0:
            D.plot()

        # print("Step {} took {} sec -- surf time = {} -- draw time = {} -- update_time = {}".format(ii, time.time()-tic,D.surf_time, D.draw_time,D.update_time))

    D.hold_until_close()
    print("number of grid points = {}".format(D.pheromone_map.size))

if __name__=='__main__':
    run()
