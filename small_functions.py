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
    return round (value / resolution) * resolution
