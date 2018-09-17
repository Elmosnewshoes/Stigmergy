""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

from ant import Ant
from domain import AntDomain
from plot import MapPlot
import numpy as np
# from overlord import Queen

class SimpleSim():
    def __init__(self, size = [1000,1000], pitch = 1, n_ants = 5):
        """ ==================
            Do a simulation of an Ant
            ================== """
        self.size = size
        self.pitch = pitch

        self.Dom = AntDomain(size, pitch,
                             food = {'location': [850,500],'radius':50},
                             nest = {'location': [150,500],'radius':50})
        self.Dom.set_gaussian(sigma = 10)
        self.Ant = Ant(limits = size, start_pos = [700,500], speed=5,)
        self.Ants = [ Ant(limits = size,
                          start_pos = 1000*np.random.rand(1,2)[0],
                          angle = 360*np.random.rand(), speed=2,
                          v_max =5, ant_id = i) for i in range(n_ants) ]
        self.Plot = MapPlot(self.Dom.Map.X,self.Dom.Map.Y)


    def draw_ant_scatter(self):
        ant_x =[]
        ant_y =[]
        sensor_left_x = []
        sensor_left_y = []
        sensor_right_x = []
        sensor_right_y = []
        for Ant in self.Ants:
            ant_x.append(Ant.pos.x)
            ant_y.append(Ant.pos.y)
            sensor_left_x.append(Ant.sensors['left'].x)
            sensor_left_y.append(Ant.sensors['left'].y)
            sensor_right_x.append(Ant.sensors['right'].x)
            sensor_right_y.append(Ant.sensors['right'].y)
        self.Plot.draw_scatter(ant_x, ant_y)
        self.Plot.draw_scatter(sensor_left_x, sensor_left_y, marker = 'o', name = 'sensor_left')
        self.Plot.draw_scatter(sensor_right_x, sensor_right_y, marker = 'o', name = 'sensor_right')

    def random_roll_sim(self,n_steps = 500, contour_interval = 1):
        """ ==================
            Simulation the pheromone accumulation with random steps
            ================== """
        # == Start loop ==
        for i in range(n_steps):
            self.Ant.random_roll(sigma_speed = 5, sigma_rotate = 0.1) # do random step
            if not self.Ant.out_of_bounds:
                self.Dom.local_add_pheromone(self.Ant.pos.vec) # add pheromone to the map
                self.Dom.update_pheromone() # update the global map
            if i%contour_interval ==0: # check if needs printing
                print("At step {:d}".format(i))
                self.Plot.draw_contour(self.Dom.Map.map) # plot the contour

            #== Draw the scatters of ant and sensors ==
            self.draw_ant_scatter()



    def gradient_sim(self,n_steps = 500, contour_interval = 1):
        """ ==================
            Simulation with pheromone based navigation
            First, prime the map, then let the ant free
            ================== """
        # == Prime the map ==
        for i in range(50):
            loc = self.size*np.random.rand(1,2)[0]
            self.Dom.add_pheromone(Q =0.125,sigma = 50,loc=loc,peak_1=True)
        self.Dom.update_pheromone()
        self.Plot.draw_contour(self.Dom.Map.map)

        #draw the nest and food source
        self.Plot.draw_scatter(self.Dom.food_location.x,
                               self.Dom.food_location.y,
                               marker = 'o', name = 'food',s=800)
        self.Plot.draw_scatter(self.Dom.nest_location.x,
                              self.Dom.nest_location.y,
                              marker = 'o', name = 'nest',s=800)


        # == loop over the simulation ==
        for i in range(n_steps):
            # get the pheromone level at ant sensor location
            for Ant in self.Ants:
                pheromone = self.Dom.get_pheromone_level(Ant.sens_loc,
                                                         islist=True)
                # perform a step
                Ant.gradient_step([Ant.observed_pheromone(pheromone[0],activation = 'linear'),
                                    Ant.observed_pheromone(pheromone[1],activation = 'linear')],
                                       gain = 0.005,
                                       SNR = 0.05)
               # add the pheromone at ant location
               # dont add pheromon when at the boundary!
                if not Ant.out_of_bounds:
                    self.Dom.local_add_pheromone(Ant.pos.vec, peak_1 = True, Q = 0.05) # add pheromone to the map
                    self.Dom.update_pheromone() # update the global map

                # == Some simulation specific intelligence ==
                if Ant.foodbound and self.Dom.inrange(Ant.pos.vec,'food'):
                    Ant.foodbound = False
                    Ant.reverse()
                    print("Found food, looking for nest")
                elif not(Ant.foodbound) and self.Dom.inrange(Ant.pos.vec, 'nest'):
                    Ant.foodbound = True
                    Ant.reverse()
                    print("Found nest, looking for food")

            # == draw stuff ==
            self.draw_ant_scatter()
            if i%contour_interval ==0:
                print("At step {:d}".format(i))
                self.Plot.draw_contour(self.Dom.Map.map)
                self.Dom.evaporate(0.97)


class MultiSim():
    """ ==================
        Do a simulation of a system of Ants
        ================== """
    def __init__(self, size = [1000,1000], pitch = 1, n_ants = 10):
        """ ==================
            WORK IN PROGRESS
            ================== """
        self.size = size
        self.pitch = pitch

        self.Dom = AntDomain(size, pitch)
        self.Dom.set_gaussian(sigma = 25)
        self.Ants = QueenAnt(Ant(limits = size, start_pos = np.dot(0.5,size), speed=10, v_max =20))
        self.Plot = MapPlot(self.Dom.Map.X,self.Dom.Map.Y)


def runSimpleSim():
    S = SimpleSim(n_ants = 5)
    # S.random_roll_sim()
    S.gradient_sim(contour_interval = 10, n_steps = 1500)

    # ==All done, lock the graph ==
    S.Plot.hold_until_close()


if __name__ == '__main__':
    runSimpleSim()
