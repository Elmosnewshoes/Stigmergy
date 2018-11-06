""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

from plugins.helper_classes import MeshMap,GaussMap, point, loc
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
        self.tmp_map = self.Map.map.copy() #explicitly duplicate the map (no pointer)

    def init_gaussian(self,sigma,significancy = 1e3):
        """ Return gaussian map object """
        """ Calculate the radius where the guassian intesity is 1/significancy
            of the value of the peak """
        R = np.asarray(np.ceil(sigma*np.sqrt(2*np.log(significancy))),dtype=int)
        Gaussian = GaussMap(resolution =self.pitch,R = R, covariance = sigma)
        # print(f"Significancy radius = {R}")
        return Gaussian

    def local_add_pheromone(self, target_pos, Q, by_volume = False):
        """ Add pheromone to the temp map:
                Q is the quantity
                If by_volume is True: add unity volume
                else add such that the peak ==1
                target_pos x,y in mm """
        if by_volume:
            alpha = 1
        else:
            alpha = 1/self.Gaussian.peak
        target = self.Map.coord2grid(target_pos)
        "span contains list with 3 elemets per axis: [start slice, center, end_slice]"
        s = self.Map.span(target,self.Gaussian.radius) #get some instructions on where to place the Gaussian
        # try:
        self.tmp_map[target.y-s['y'][1]+s['y'][0]:target.y+s['y'][2]-s['y'][1],
                    target.x-s['x'][1]+s['x'][0]:target.x+s['x'][2]-s['x'][1]
                    ]+= self.Gaussian.map[s['y'][0]:s['y'][2],s['x'][0]:s['x'][2]]
        # except Exception as error:
        #     print(target_pos)
        #     raise error

    def probe_pheromone(self,probe_loc):
        " Return the pheromone level based on xy in mm, 0 if out of bounds "
        if probe_loc.x<0 or probe_loc.y <0 or (probe_loc.vec > self.size.vec).any():
            return 0
        else:
            probe_point = self.Map.coord2grid(probe_loc)
            return self.Map.map[probe_point.y,probe_point.x]

    def set_target_pheromone(self, Q):
        """ Desired total volume of the pheromone on the map """
        self.target_pheromone = Q

    def evaporate(self, xsi =0):
        """ Caution!! tmp map is evaporated, not the main """
        " Caution: neglecting volume of grid"
        if xsi == 0:
            self.tmp_map = self.tmp_map.dot(self.target_pheromone/self.tmp_map.sum())
        else:
            self.tmp_map = self.tmp_map.dot(xsi)

    def update_pheromone(self):
        """ Add the temp map to the global map """
        "Explicit copy, no pointer"
        self.Map.map = np.copy(self.tmp_map)

    def inrange(self,pnt, target = 'food'):
        """ Check if point is within the defined food or nest area """
        if target == 'food':
            return np.linalg.norm(pnt.vec-self.food_location.vec) <= self.food_radius
        else:
            return np.linalg.norm(pnt.vec-self.nest_location.vec) <= self.nest_radius


def run():
    domain_dict = {'size': [1000,500],
                   'pitch': 1,
                   'start_concentration':1,
                   'nest':{'location': [250,250],'radius':50},
                   'food':{'location': [750,250],'radius':50}}
    D = Domain(**domain_dict)
    D.Gaussian = D.init_gaussian(sigma=15)
    print(D.Map)
    print(D.Gaussian.peak)
    print(D.Gaussian.entropy)
    print(D.Gaussian)
    xy = point(100,100)
    D.local_add_pheromone(xy, 2,True)
    D.update_pheromone()
    print(D.probe_pheromone(xy))
    assert D.probe_pheromone(xy) == D.Map.map.max()#check if all works correctly
    print(D.tmp_map.sum())
    D.evaporate(0.9)
    print(D.tmp_map.max())
    D.set_target_pheromone(10)
    D.evaporate()
    print(D.tmp_map.max())
    print(D.tmp_map.sum())
    xy = point(250,500)
    print(D.food_location.vec)
    print("Point {} is in range of food? {}".format(xy,D.inrange(xy,'food')))
    D.local_add_pheromone(point(301.13,559.72),1)

if __name__ == '__main__':
    run()
