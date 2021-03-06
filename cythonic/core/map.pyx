# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp
from cython.parallel cimport prange
cimport numpy as np
import numpy as np
from cythonic.plugins.positions cimport point, index, map_range
from libc.math cimport lrint # round double, cast as long
from libc.math cimport log2 as clog2

cdef class Map:
    """ base class for a meshgrid and some supporting functions """
    "map == 2D array map[x,y]"

    cdef readonly map_range span(self,unsigned long *Ix, unsigned long *Iy,double *R):
        """ return the upper limits of a meshmap that fits in self.map
            I as index pair xy -> grid coords[uint, uint],
            R as offset in mm """
        cdef map_range XY # store result
        cdef unsigned long R_int = self.to_grid(R)
        XY.x[1] = R_int
        XY.y[1] = R_int
        if Ix[0] +R_int+1 > self.lim.x: # ubound(x)
            XY.x[2] = R_int+self.lim.x+1-Ix[0]
        else: XY.x[2] = 2*R_int+1
        if Iy[0] +R_int+1 > self.lim.y: #ubound(y)
            XY.y[2] = R_int+self.lim.y+1-Iy[0]
        else: XY.y[2] = 2*R_int+1
        if Ix[0] < R_int: XY.x[0] = R_int - Ix[0] #lbound(x)
        else: XY.x[0] = 0
        if Iy[0] < R_int: XY.y[0] = R_int - Iy[0] #lbound(y)
        else: XY.y[0] = 0
        return XY

    cdef readonly unsigned long to_grid(self, double * x):
        " round point in mm to grid index "
        return lrint(x[0]/self.pitch)
    cdef readonly double to_mm(self,unsigned long * x):
        " convert grid index to location in mm "
        return <double>self.pitch*x[0]

    cdef readonly double sum(self):
        " manually sum a map using multiple threads (faster than NumPy)"
        cdef double s = 0
        cdef unsigned int i,j,I,J
        I = self.map.shape[0]
        J = self.map.shape[1]
        for i in prange(I, nogil=True,schedule='static', chunksize=10):
            for j in range(J):
                s+= self.map[i,j]
        return s

    cdef readonly double max(self):
        " manually find max, omitting safety/sanity checks makes it faster than numpy"
        " assuming strictly nonnegative entries "
        cdef double m = 0
        cdef unsigned int i,j,I,J
        I = self.map.shape[0]
        J = self.map.shape[1]
        for i in range(I):
            for j in range(J):
                if self.map[i,j]> m:
                    m=self.map[i,j]
        return m

    cdef readonly double entropy(self):
        cdef unsigned int i,j,I,J
        (I,J) = self.map.shape[:2] # domain
        # cdef double h = 0. # entropy
        cdef double T = self.sum() # sum of pheromones
        if T <= 0.0:
            raise ValueError('Sum of pheromone map <= 0')
        cdef unsigned int threads = 8
        cdef double[:] h = np.zeros(I) #temporary store entropy per line
        for i in prange(I,nogil=True,schedule='static', chunksize=10):
            for j in range(J):
                # if self.map[i,j]<= 1e-20:
                    # " check if nothing goes wrong here "
                    # raise ValueError('Error calculating the entropy of the map: log of nearzero number is ill-defined')
                h[i]-= self.map[i,j]/T*clog2(self.map[i,j]/T)
        return np.sum(h)

    def __repr__(self):
        " print useful information "
        return "Map with size ({}x{}), pitch = {};".format(
            self.dim.x, self.dim.y,self.resolution)

    def new(self, double[:] dim, double resolution):
        " assume dim is vector[2]=> [double x, double y]"
        self.dim = point(dim[0], dim[1])
        self.pitch = resolution
        self.lim = index(self.to_grid(&self.dim.x),self.to_grid(&self.dim.y))

        self.mesh_x, self.mesh_y = np.meshgrid(\
                np.arange(0,(<double>self.lim.x)*resolution+resolution, resolution),
                np.arange(0,(<double>self.lim.y)*resolution+resolution, resolution))
        self.map = np.ones((self.lim.y+1,self.lim.x+1),dtype = np.float_)

cdef class MeshMap(Map):
    " Map wrapper "
    def __cinit__(self,double[:] dim, double resolution):
        self.new(dim,resolution)

cdef class GaussMap(Map):
    def __cinit__(self,double resolution, double R, double covariance):
        self.radius = R
        # print(f'New gaussian with radius: {R}')
        dim = np.array([np.ceil(self.radius/resolution)*resolution*2+resolution,np.ceil(self.radius/resolution)*resolution*2+resolution], dtype = np.float_)
        self.new(dim,resolution)
        self.map = self.bivariate_normal(sigmax=np.sqrt(covariance),sigmay=np.sqrt(covariance),
            mux = self.dim.x/2, muy=self.dim.y/2, sigmaxy=0)
        # print(f'Map shape is: {np.array(self.map).shape[0:2]}')
        self.volume = np.array(self.map).sum()*self.pitch**2
        self.peak = np.array(self.map).max()
        # print(f"Volume of the gaussian = {self.volume}")
        # print(f"Max of gaussian = {self.peak}")

    def bivariate_normal(self,sigmax=1.0, sigmay=1.0,
                         mux=0.0, muy=0.0, sigmaxy=0.0):
        """
        X (meshgrid),Y (meshgrid), sigmax (scalar), sigmay (scalar), mux (scalar),
        muy (scalar) , sigmaxy(scalar)
        FROM https://github.com/matplotlib/matplotlib/blob/81e8154dbba54ac1607b21b22984cabf7a6598fa/lib/matplotlib/mlab.py#L1866
        Bivariate Gaussian distribution for equal shape *X*, *Y*.
        See `bivariate normal
        <http://mathworld.wolfram.com/BivariateNormalDistribution.html>`_
        at mathworld.
        """
        X = np.array(self.mesh_x)
        Y = np.array(self.mesh_y)
        Xmu = X-mux
        Ymu = Y-muy

        rho = sigmaxy/(sigmax*sigmay)
        z = Xmu**2/sigmax**2 + Ymu**2/sigmay**2 - 2*rho*Xmu*Ymu/(sigmax*sigmay)
        denom = 2*np.pi*sigmax*sigmay*np.sqrt(1-rho**2)
        # return np.exp(-z/(2*(1-rho**2))) / denom
        return np.exp(-z/(2*(1-rho**2))) # peak of gaussian ==1
