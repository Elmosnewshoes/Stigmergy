import numpy as np

def class_tuple2nparray(list_of_xy):
    xys = np.zeros((len(list_of_xy),2))
    for i in range(len(list_of_xy)):
        xys[i] = [list_of_xy[i].x, list_of_xy[i].y]
    return xys

def T_matrix( theta ):
    """ ==============================
        Transformation matrix for specified angle [theta]
        in degrees: [X_new, Y_new] = [X,Y]*T_matrix'
        As above, clockwise rotation is positive
        ============================== """
    theta  = np.radians(theta)
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c,-s), (s, c)))
    # return np.matrix([[math.cos(theta*math.pi/180), -math.sin(theta*math.pi/180)],
    #                  [math.sin(theta*math.pi/180), math.cos(theta*math.pi/180)]])

def lin_fun(x, noise = 0):
    return x+(2*noise*np.random.rand()-1)


def bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0,
                     mux=0.0, muy=0.0, sigmaxy=0.0):
    """
    FROM https://github.com/matplotlib/matplotlib/blob/81e8154dbba54ac1607b21b22984cabf7a6598fa/lib/matplotlib/mlab.py#L1866
    Bivariate Gaussian distribution for equal shape *X*, *Y*.
    See `bivariate normal
    <http://mathworld.wolfram.com/BivariateNormalDistribution.html>`_
    at mathworld.
    """
    Xmu = X-mux
    Ymu = Y-muy

    rho = sigmaxy/(sigmax*sigmay)
    z = Xmu**2/sigmax**2 + Ymu**2/sigmay**2 - 2*rho*Xmu*Ymu/(sigmax*sigmay)
    denom = 2*np.pi*sigmax*sigmay*np.sqrt(1-rho**2)
    return np.exp(-z/(2*(1-rho**2))) / denom

def circle_scatter(center,R):
    " center as in [x, y] location "
    xy = np.empty((0,2)) # empty list of lists [x, y]
    for i in range(0,360,10):
        " Create scatter "
        xy = np.vstack((xy,np.array(center)
                            +T_matrix(i).dot([R,0])))
    return xy
