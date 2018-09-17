""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """


import small_functions as fun
import numpy as np
import matplotlib.mlab as mlab

class MeshMap():
    """ ===============
        Handle the map and useful small_functions
        X,Y are in local coordinates (mm by default)
        x1,x2 are corresponding grid coordinates
        =============== """
    def __init__(self, dim, resolution = 1, base = [0,0]):
        if type(dim) is list or type(dim) == type(np.array([])):
            self.dim = fun.Point(dim)
        elif type(dim) is int:
            self.dim = fun.Point([dim,dim])
        else:
            self.dim = dim

        # base, dim in mm
        if type(base) is list:
            self.base = fun.Point(base)
        else:
            self.base = base

        # set limits in pixel/grid coordinates
        self.lim = fun.Point(np.round((np.array(self.dim.vec)-np.array(self.base.vec))
                                        /resolution + resolution, 0))
        self.low_lim = fun.Point(np.round(np.array(self.base.vec)/resolution, 0))

        self.pitch = resolution

        self._spanX = np.arange(self.base.x,self.dim.x+resolution, resolution)
        self._spanY = np.arange(self.base.y,self.dim.y+resolution, resolution)
        self.X, self.Y = np.meshgrid(self._spanX,self._spanY)

        self._map = np.zeros(self.X.shape)

    def coord2grid(self,coord):
        if type(coord) is fun.Point:
            return np.array(np.dot(coord.vec,1/self.pitch).astype(int))
        elif type(coord) is list:
            return np.array(np.dot(coord,1/self.pitch).astype(int))
        elif type(coord) is float or type(coord) is int:
            return int(float(coord/self.pitch))
        else:
            return coord/self.pitch

    def grid2coord(self, loc):
        if type(loc) is fun.Point:
            return fun.Point(np.array(np.dot(loc.vec,self.pitch).astype(float)))
        elif type(loc) is list and len(loc) ==2:
            return fun.Point(np.array(np.dot(loc,self.pitch).astype(float)))
        elif type(loc) is float or type(loc) is int:
            return float(loc*self.pitch)
        else:
            return loc/self.pitch

    @property
    def map(self, ):
        return self._map
    @map.setter
    def map(self,map):
        self._map = map

    def init_map(self,map_type,**kwargs):
        "Set the map type according to specified string"
        if map_type == 'identity':
            self._map = np.identity(min(self.dim.x,self.dim.y))
        elif map_type == 'zero':
            pass
        elif map_type == 'random':
            self._map = np.random.rand(self.dim.x,self.dim.y)
        elif map_type == 'gaussian':
            self._map = self.pitch*self.pitch*mlab.bivariate_normal(self.X,self.Y, kwargs['covariance'],
                                              kwargs['covariance'],
                                              (self.dim.x-self.base.x)/2,
                                              (self.dim.y-self.base.y)/2)


    def span(self,base = 0, **kwargs):
        """ ===========
            Return indexes (pixel/grid coordinates) for the map centered around 'base'
            going from '[base - span]' to and including '[base + span]'
            [base] in absolute coordinates
            =========== """
        error = False # required in output
        limit = ''
        ax = ''
        if 'axis' in kwargs:
            ax = kwargs['axis'].upper() # need to return this
            if ax == 'X' or ax =='X1':
                'X-axis: first component in list/matrix'
                up_lim = self.lim.x
                low_lim = self.low_lim.x
            else:
                'Y-axis, second component (index 1) in list/matrix'
                up_lim = self.lim.y
                low_lim = self.low_lim.y
        else:
            'no axis specified: generalizing'
            up_lim = max(self.map.shape)
            low_lim = 0

        if 'span' in kwargs:
            # check limits
            if int(base/self.pitch) - int(kwargs['span']) < low_lim:
                'indicate lower bound error'
                error = True
                limit = 'lower'
            elif int(base/self.pitch) + int(kwargs['span'])+1 > up_lim:
                'upper bound error'
                error = True
                limit = 'upper'

            low_lim  = max(low_lim,int(base/self.pitch) - int(kwargs['span']))
            up_lim = min(up_lim, int(base/self.pitch) + int(kwargs['span'])+1)
            span = [int(low_lim),int(up_lim)] # return this
        else:
            span = int(base/self.pitch)

        return [span,{'error': error,
                'axis' : ax,
                'limit': limit}]


def run():
    M = MeshMap(dim=[10,10], resolution = 0.5)
    # M._map = np.identity(10)
    # print(M.map.shape)
    print(M.lim.vec)
    M.init_map(map_type ='gaussian', covariance = 0.25)
    i,j = np.where(M.map==M.map.max())
    print('{},{}'.format(M.X[0][i][0],M.Y[j][0][0]))
    print(M.span(base=5, span =3, axis='X'))
    print(M.X)

    print(M.coord2grid(1))
    print(M.grid2coord([1,1]))

if __name__ == '__main__':
    run()
