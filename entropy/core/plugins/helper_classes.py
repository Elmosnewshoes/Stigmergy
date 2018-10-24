import numpy as np
from helper_functions import bivariate_normal

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
    def __init__(self,dim,resolution, R=0):
        """ Dim: x and y limits in mm
            resolution: points per mm
            R: radius in X,Y direction [mm], if nonzero, overwrites dim """

        " Properties "
        if R ==0:
            self.dim = point(*dim) # in mm
        else:
            self.dim = point(2*R,2*R) # in mm
        self.pitch = resolution # points per mm
        self.lim = loc(*np.round(np.dot(self.dim.vec,1/resolution),0)+[1,1])

        self.mesh_x, self.mesh_y = np.meshgrid(
            np.arange(0,self.lim.x*resolution, resolution),
            np.arange(0,self.lim.y*resolution, resolution),
        )
        self.map = np.zeros(self.mesh_x.shape)

    def set_map(self,map_type,**type_kwargs):
        if map_type =='identity':
            self.map = np.identity(min(self.dim.x,self.dim.y))
        elif map_type == 'zero':
            self.map = np.zeros(self.mesh_x.shape)
        elif map_type == 'random':
            if kwargs['gain']:
                gain = kwargs['gain']
            else:
                gain = 1
            self.map = gain*np.random.rand(self.dim.x,self.dim.y)
        elif map_type == 'gaussian':
            self.map = self.pitch**2*bivariate_normal(self.mesh_x,self.mesh_y, type_kwargs['covariance'],
                                              type_kwargs['covariance'],
                                              (self.dim.x)/2,
                                              (self.dim.y)/2)


    def coord2grid(self, pnt):
        """ return xy in grid coordinates (loc tuple) [absolute -- integer]
            from point coordinates (point tuple) [mm -- float] """

        """ Warning: floating point representation can cause
                unexpected rounding results !!! """
        return loc(*pnt.vec.dot(1/self.pitch).round(0).astype(int))

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
            R as offset in grid coords [int] """
        x_min,y_min = [0,0]
        x_max,y_max = [2*R+1, 2*R+1]
        if l.x +R+1 > self.lim.x: x_max = x_max-(l.x+R - self.lim.x)-1
        if l.y +R+1 > self.lim.y: y_max = y_max-(l.y+R - self.lim.y)-1
        if l.x -R < 0: x_min = R - l.x
        if l.y -R < 0: y_min = R - l.y
        return {'x': [x_min,R,x_max],
                 'y': [y_min,R,y_max]}



def run():
    """ test stuff """
    p = point(*[3,3])
    l = loc(*[3,3])
    print(p.vec)
    print(l.vec)
def test_mesmap():
    M = MeshMap([20,20], 0.5)
    print(M.lim.vec)
    R = 2
    target = loc(10,10)
    s = M.span(target ,R)
    print(s)
    X = MeshMap([1,1], 2, 4)
    print(s['x'])
    print(s['y'])
    print(M.map)
    X.set_map(map_type = 'gaussian',covariance = 4)
    print(X.map)
    tmp_map = X.map[s['y'][0]:s['y'][2],s['x'][0]:s['x'][2]]
    print(tmp_map.shape)
    print(M.map[target.y-s['y'][1]+s['y'][0]:target.y+s['y'][2]-s['y'][1],
                target.x-s['x'][1]+s['x'][0]:target.x+s['x'][2]-s['x'][1]].shape)
    print(s)
    print(target.x-s['x'][1]+s['x'][0])
    print(target.x+s['x'][2]-s['x'][1])
    print(target.y-s['y'][1]+s['y'][0])
    print(target.y+s['y'][2]-s['y'][1])

    M.map[target.y-s['y'][1]+s['y'][0]:target.y+s['y'][2]-s['y'][1],
                target.x-s['x'][1]+s['x'][0]:target.x+s['x'][2]-s['x'][1]] += tmp_map
    print(M.map)
    print(M.grid2coord(loc(1,1)))
    print(M.coord2grid(point(1,1)))
if __name__ == '__main__':
    test_mesmap()
