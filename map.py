import small_functions as fun
import numpy as np
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


def run():
    M = MeshMap(dim=[10,10], resolution = 0.5)
    # M._map = np.identity(10)
    # print(M.map.shape)
    # print(M.lim.vec)
    M._covariance = 0.25
    M.map = 'gaussian'
    i,j = np.where(M.map==M.map.max())
    print('{},{}'.format(M.X[0][i][0],M.Y[j][0][0]))
    # print(M.span(base=5, span =3, axis='X'))

if __name__ == '__main__':
    run()
