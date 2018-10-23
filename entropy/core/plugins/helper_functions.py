import numpy as np
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
