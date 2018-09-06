import math
import numpy as np
from collections import namedtuple

def gaussian(X,Y, mu, sig):
    """ ==============================
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
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        'Print useful descripition'
        return "'Point' x = {0:.5f}, y = {1:.5f};".format(self._x, self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def vec(self):
        # return the position coordinates as row vector
        return [self._x,self._y]
    @vec.setter
    def vec(self,vec):
        if len(vec)== 2: #assumed: list [x,y]
            self._x = vec[0]
            self._y = vec[1]
        else: #numpy matrix
            self._x = vec[0,0]
            self._y = vec[0,1]

def T_matrix( theta ):
    """ ==============================
        Transformation matrix for specified angle [theta]
        in degrees: [X_new, Y_new] = [X,Y]*T_matrix
        As above, clockwise rotation is positive
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
