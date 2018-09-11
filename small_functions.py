import math
import numpy as np
from collections import namedtuple
import small_functions as fun
import matplotlib.mlab as mlab

class MeshMap():
    def __init__(self, dim, resolution = 1, base = [0,0], **kwargs):
        if type(dim) is list:
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

        if 'covariance' in kwargs:
            self._covariance = kwargs['covariance']

    @property
    def map(self, ):
        return self._map
    @map.setter
    def map(self,shape):
        "Set the map type according to specified string"
        if shape == 'identity':
            self._map = np.identity(min(self.dim.x,self.dim.y))
        elif shape == 'zero':
            pass
        elif shape == 'random':
            self._map = np.random.rand(self.dim.x,self.dim.y)
        elif shape == 'gaussian':
            self._map = mlab.bivariate_normal(self.X,self.Y, self._covariance,
                                              self._covariance,
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
        if 'axis' in kwargs:
            ax = kwargs['axis'].upper() # need to return this
            if ax == 'X':
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
            span = np.arange(low_lim,up_lim,1) # return this
        else:
            span = int(base/self.pitch)

        return {'span' : span,
                'error': error,
                'axis' : ax,
                'limit': limit}


def gaussian(X,Y, mu, sig):
    """ ==============================
        NO LONGER IN USE
        Redundant, mlab.bivariate_normal does the same but faster
        calculate the value of a 2D NORMALIZED gaussian function
        e.g.: Volume of f(x,y)==1
        ============================== """
    A = sig*sig*2*np.pi
    G = np.exp(-np.add(np.power(X-mu[0],2)/(2*np.power(sig,2)),np.power(Y-mu[1],2)/(2*np.power(sig,2))))
    return G/A


def roundPartial (value, resolution):
    """ ==============================
        round a [value] to the specified [resolution]
        ============================== """
    return round (value / resolution) * resolution

class Point():
    """ =====================
        Defining method vec() that returns the point coordinates in a row vector
        ===================== """
    def __init__(self, *args):
        self._x = 0
        self._y = 0

        if len(args) == 2:
            self._x = args[0]
            self._y = args[1]
        elif len(args) == 1:
            l = args[-1]
            self._x = l[0]
            self._y = l[1]
        else:
            raise Exception('Unexpected amount of input arguments: {}'.format(len(args)))
        self.type = ''
        self.set_type()

    def set_type(self,):
        if np.mod(self._x, 1) ==0 and np.mod(self._y,1)==0:
            self.type = 'int'
        else:
            self.type = 'float'


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        'Print useful descripition'
        if self.type == 'int':
            return "'Point' x = {}, y = {};".format(self._x, self._y)
        else:
            return "'Point' x = {0:.5f}, y = {1:.5f};".format(self._x, self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if np.mod(x,1)==0:
            self._x = int(x)
        else:
            self._x = x
        self.set_type()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if np.mod(y,1)==0:
            self._y = int(y)
        else:
            self._y = y
        self.set_type()

    @property
    def vec(self):
        # return the position coordinates as row vector
        if self.type =='int':
            return [int(self._x), int(self._y)]
        else:
            return [self._x,self._y]

    @vec.setter
    def vec(self,vec):
        if len(vec)== 2: #assumed: list [x,y]
            self.x = vec[0]
            self.y = vec[1]
        else: #numpy matrix
            self.x = vec[0,0]
            self.y = vec[0,1]

def T_matrix( theta ):
    """ ==============================
        Transformation matrix for specified angle [theta]
        in degrees: [X_new, Y_new] = [X,Y]*T_matrix
        As above, clockwise rotation is posi                tive
        ============================== """
    return np.matrix([[math.cos(theta*math.pi/180), -math.sin(theta*math.pi/180)],
                     [math.sin(theta*math.pi/180), math.cos(theta*math.pi/180)]])

if __name__ == '__main__':
    print([1,0]*T_matrix(30))
    # P = Point(1,1)
    # P.vec = [1,2]
    # print(P.x)
    # P.x = 10
    # print(P.x)

    M = MeshMap(dim=[10,10], resolution = 0.5)
    # M._map = np.identity(10)
    # print(M.map.shape)
    # print(M.lim.vec)
    M._covariance = 0.25
    M.map = 'gaussian'
    i,j = np.where(M.map==M.map.max())
    print('{},{}'.format(M.X[0][i][0],M.Y[j][0][0]))
    # print(M.span(base=5, span =3, axis='X'))
