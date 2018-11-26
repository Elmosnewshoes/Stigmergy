cimport numpy as np
import numpy as np
from cythonic.plugins.positions cimport point, index, map_range
from libc.math cimport lrint # round double, cast as long

cdef class Map:
    """ base class for a meshgrid and some supporting functions """

    cdef readonly map_range span(self,unsigned long[::1] I,double * R):
        """ return the upper limits of a meshmap that fits in self.map
            I as index pair xy -> grid coords[uint, uint],
            R as offset in mm """
        cdef map_range XY # store result
        cdef unsigned long R_int = self.to_grid(R)
        XY.x[1] = R_int
        XY.y[1] = R_int
        if I[0] +R_int+1 > self.lim.cx(): # ubound(x)
            XY.x[2] = R_int-I[0]+self.lim.cx()+1
        else: XY.x[2] = 2*R_int+1
        if I[1] +R_int+1 > self.lim.cy(): #ubound(y)
            XY.y[2] = R_int -I[1]+self.lim.cy()+1
        else: XY.y[2] = 2*R_int+1
        if I[0] < R_int: XY.x[0] = R_int - I[0] #lbound(x)
        else: XY.x[0] = 0
        if I[1] < R_int: XY.y[0] = R_int - I[1] #lbound(y)
        else: XY.y[0] = 0
        return XY

    cdef readonly unsigned long to_grid(self, double * x):
        " round point in mm to grid index "
        return lrint(x[0]/self.pitch)

    cdef readonly double to_mm(self,unsigned long * x):
        " convert grid index to location in mm "
        return <double>self.pitch*x[0]

    def __repr__(self):
        " print useful information "
        return "Map with size ({}x{}), pitch = {};".format(
            self.dim.x, self.dim.y,self.resolution)

    def new(self, double[:] dim, double resolution):
        " assume dim is vector[2]=> [double x, double y]"
        self.dim = point(dim[0], dim[1])
        self.pitch = resolution
        self.lim = index(self.to_grid(&self.dim.xy[0]),self.to_grid(&self.dim.xy[1]))

        self.mesh_x, self.mesh_y = np.meshgrid(\
                np.arange(0,(<double>self.lim.x)*resolution+resolution, resolution),
                np.arange(0,(<double>self.lim.y)*resolution+resolution, resolution))
        self.map = np.ones((self.lim.x+1,self.lim.y+1),dtype = np.float_)

cdef class MeshMap(Map):
    " Map wrapper "
    def __cinit__(self,double[:] dim, double resolution):
        self.new(dim,resolution)

cdef class GaussMap(Map):
    def __cinit__(self,double resolution, double R, double covariance):
        self.radius = np.ceil(R,dtype = np.float_)
        dim = np.array([self.radius*2,self.radius*2], dtype = np.float_)
        self.new(dim,resolution)
        self.map = self.bivariate_normal(sigmax=covariance,sigmay=covariance,
            mux = self.dim.x/2, muy=self.dim.y/2, sigmaxy=0)
        self.volume = np.array(self.map).sum()*self.pitch**2
        self.peak = np.array(self.map).max()

        print(f"volume = {self.volume}\n peak at {self.peak}")

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
        return np.exp(-z/(2*(1-rho**2))) / denom
