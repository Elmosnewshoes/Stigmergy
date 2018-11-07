""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

from core.plugins.helper_classes import MeshMap,GaussMap, point, loc
import numpy as np


class Domain():
    """ Domain class, idea is that any input coordinates are in mm,
        the class methods do the conversion to grid coordinates """
    def __init__(self, size, pitch,nest={}, food={}):
        """ Simulation playground """
        self.size = point(*size) # xy in mm (point object)
        self.pitch = pitch
        if nest:
            self.nest_location = point(*nest['location'])
            self.nest_radius = nest['radius']
        if food:
            self.food_location = point(*food['location'])
            self.food_radius = food['radius']
        self.Map = MeshMap(dim = size, resolution=pitch)
        self.dim = loc(*self.Map.map.shape)
        # self.tmp_map = self.Map.map.copy() #explicitly duplicate the map (no pointer)

    def init_gaussian(self,sigma,significancy = 1e3):
        """ Return gaussian map object """
        """ Calculate the radius where the guassian intesity is 1/significancy
            of the value of the peak """
        R = np.asarray(np.ceil(sigma*np.sqrt(2*np.log(significancy))),dtype=int)
        Gaussian = GaussMap(resolution =self.pitch,R = R, covariance = sigma)
        return Gaussian

    def local_add_pheromone(self, target_pos, Q):
        """ Add pheromone to the temp map:
                Q is the quantity
                target_pos x,y in mm """
        target = self.Map.coord2grid(target_pos)
        "span contains list with 3 elemets per axis: [start slice, center, end_slice]"
        s = self.Map.span(target,self.Gaussian.radius) #get instructions on where to place the Gaussian
        self.Map.map[target.y-s['y'][1]+s['y'][0]:target.y+s['y'][2]-s['y'][1],
                    target.x-s['x'][1]+s['x'][0]:target.x+s['x'][2]-s['x'][1]
                    ]+= Q*self.Gaussian.map[s['y'][0]:s['y'][2],s['x'][0]:s['x'][2]]

    def probe_pheromone(self,probe_point):
        " Return the pheromone level based on xy in mm, 0 if out of bounds "
        if probe_point.x<0 or probe_point.y <0 or (probe_point.vec > self.size.vec).any():
            return 0
        else:
            probe_loc = self.Map.coord2grid(probe_point)
            return self.Map.map[probe_loc.y,probe_loc.x]

    def set_target_pheromone(self, Q):
        """ Desired total volume of the pheromone on the map """
        self.target_pheromone = Q

    def evaporate(self, xsi =0):
        """ Map is evaporated """
        " Caution: neglecting volume of grid"
        if xsi == 0:
            # self.tmp_map = self.tmp_map.dot(self.target_pheromone/self.tmp_map.sum())
            self.Map.map = self.Map.map.dot(self.target_pheromone/self.Map.map.sum())
        else:
            # self.tmp_map = self.tmp_map.dot(xsi)
            self.Map.map = self.Map.map.dot(xsi)

    def inrange(self,pnt, target = 'food'):
        """ Check if point is within the defined food or nest area """
        if target == 'food':
            return np.linalg.norm(pnt.vec-self.food_location.vec) <= self.food_radius
        else:
            return np.linalg.norm(pnt.vec-self.nest_location.vec) <= self.nest_radius
