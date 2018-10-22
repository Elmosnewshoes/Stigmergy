def T_matrix( theta ):
    """ ==============================
        Transformation matrix for specified angle [theta]
        in degrees: [X_new, Y_new] = [X,Y]*T_matrix
        As above, clockwise rotation is posi                tive
        ============================== """
    return np.matrix([[math.cos(theta*math.pi/180), -math.sin(theta*math.pi/180)],
                     [math.sin(theta*math.pi/180), math.cos(theta*math.pi/180)]])
