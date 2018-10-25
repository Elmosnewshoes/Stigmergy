import numpy as np
if __name__ == '__main__':
    from helper_functions import bivariate_normal
else:
    from plugins.helper_functions import bivariate_normal

class point:
    """ holds xy coordinates in mm (floats)"""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @property
    def vec(self):
        return np.array((self.x, self.y))
    def __repr__(self):
        return "'x': {x}; 'y': {y}".format(x=self.x, y = self.y)

class loc(point):
    """ holds xy coordinates in grid points (ints (unsigned))"""
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


class MeshMap:
    def __init__(self,dim,resolution):
        """ Dim: x and y limits in mm
            resolution: points per mm
         """

        " Properties "
        if type(dim) is list:
            self.dim = point(*dim) # in mm
        else:
            self.dim = dim #assume already point object
        self.pitch = resolution # points per mm
        self.lim = loc(*np.round(np.dot(self.dim.vec,1/resolution),0)+[1,1])

        self.mesh_x, self.mesh_y = np.meshgrid(
            np.arange(0,self.lim.x*resolution, resolution),
            np.arange(0,self.lim.y*resolution, resolution),
        )
        self.map = np.zeros(self.mesh_x.shape)

    def coord2grid(self, pnt):
        """ return xy in grid coordinates (loc tuple) [absolute -- integer]
            from point coordinates (point tuple) [mm -- float] """

        """ Warning: floating point representation can cause
                unexpected rounding results !!! """
        return loc(*np.rint(pnt.vec.dot(1/self.pitch)))

    def grid2coord(self, l):
        """ return xy in local coordinates (point tuple) [mm -- float]
            from grid coords (loc tuple) [absolute -- integer] """
        return point(*l.vec.dot(self.pitch))

    @property
    def entropy(self):
        """ Calculate the shannon entropy of the whole map """
        T = self.map.sum()# sum of pheromones
        M = self.map[self.map > 1e-6]# explicitly avoid zeros as log(0) is not defined
        return -np.multiply(M/T,np.log2(M/T)).sum() # return sum(M/T * log2(M/T))

    def span(self, l, R):
        """ return the upper limits of a meshmap that fits in self.map
            loc as loc tuple xy -> grid coords[int, int],
            R as offset in mm """
        R = np.asscalar(np.asarray(np.rint(R/self.pitch),dtype=int))
        x_min,y_min = [0,0]
        x_max,y_max = [2*R+1, 2*R+1]
        if l.x +R+1 > self.lim.x: x_max = x_max-(l.x+R - self.lim.x)-1
        if l.y +R+1 > self.lim.y: y_max = y_max-(l.y+R - self.lim.y)-1
        if l.x -R < 0: x_min = R - l.x
        if l.y -R < 0: y_min = R - l.y
        return {'x': [x_min,R,x_max],
                 'y': [y_min,R,y_max]}
    def __repr__(self):
        return "A map with size {}x{}; with resolution {}".format(*self.map.shape,self.pitch)

class GaussMap(MeshMap):
    def __init__(self,resolution,R,covariance):
        """ Initialize the MeshMap, dim based on R, overwrite the map property """
        " R in mm "
        self.radius = R
        dim = point(2*R,2*R)
        super().__init__(dim,resolution)
        self.map = self.gaussian_map(covariance) # override the zero map
        self.volume = self.map.sum()*self.pitch**2
        self.peak = self.map.max()

    def gaussian_map(self, cov):
        """ Return gaussian with volume ==1 """
        return bivariate_normal(self.mesh_x,self.mesh_y, cov,
                                 cov,(self.dim.x)/2,(self.dim.y)/2)

def run():
    """ test stuff """
    p = point(*[3,3])
    l = loc(*[3,3])
    print(p.vec)
    print(l.vec)
def test_mesmap():
    M = MeshMap([20,20], 2)
    print(M.lim.vec)
    R = 2
    target = loc(10,10)
    s = M.span(target ,R)
    print(s)
    print(s['x'])
    print(s['y'])
    print(M.map)
    X = GaussMap(resolution = 2,R = R, covariance = 2)
    tmp_map = X.map[s['y'][0]:s['y'][2],s['x'][0]:s['x'][2]]
    print(tmp_map)
    print(M.map[target.y-s['y'][1]+s['y'][0]:target.y+s['y'][2]-s['y'][1],
                target.x-s['x'][1]+s['x'][0]:target.x+s['x'][2]-s['x'][1]].shape)
    print(s)
    print(target.x-s['x'][1]+s['x'][0])
    print(target.x+s['x'][2]-s['x'][1])
    # print(target.y-s['y'][1]+s['y'][0])
    # print(target.y+s['y'][2]-s['y'][1])

    M.map[target.y-s['y'][1]+s['y'][0]:target.y+s['y'][2]-s['y'][1],
                target.x-s['x'][1]+s['x'][0]:target.x+s['x'][2]-s['x'][1]] += tmp_map
    print(M.map)
    print(M.grid2coord(loc(1,1)))
    print(M.coord2grid(point(3,3)))
    print(M)
if __name__ == '__main__':
    test_mesmap()
