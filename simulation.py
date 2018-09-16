from ant import Ant
from domain import AntDomain
from plot import MapPlot
import numpy as np
# from overlord import Queen

class SimpleSim():
    def __init__(self, size = [1000,1000], pitch = 1):
        """ ==================
            Do a simulation of an Ant
            ================== """
        self.size = size
        self.pitch = pitch

        self.Dom = AntDomain(size, pitch)
        self.Dom.set_gaussian(sigma = 10)
        self.Ant = Ant(limits = size, start_pos = np.dot(0.5,size), speed=10, v_max =20)
        self.Plot = MapPlot(self.Dom.Map.X,self.Dom.Map.Y)



    def random_roll_sim(self,n_steps = 500, contour_interval = 1):
        """ ==================
            Simulation the pheromone accumulation with random steps
            ================== """
        self.Ant.azimuth = 90
        for i in range(n_steps):
            self.Ant.random_roll(sigma_speed = 5, sigma_rotate = 0.1) # do random step
            self.Dom.local_add_pheromone(self.Ant.pos.vec) # add pheromone to the map
            self.Dom.update_pheromone() # update the global map
            if i%contour_interval ==0:
                self.Plot.draw_contour(self.Dom.Map.map) # plot the contour
            self.Plot.draw_scatter(self.Ant.pos.x, self.Ant.pos.y) # draw ant location
            self.Plot.draw_scatter(self.Ant.sensors['left'].x, self.Ant.sensors['left'].y, marker = 'o', name = 'sensor_left')
            self.Plot.draw_scatter(self.Ant.sensors['right'].x, self.Ant.sensors['right'].y, marker = 'o', name = 'sensor_right')

        # Lock the graph
        self.Plot.hold_until_close()



    def gradient_sim(self,):
        """ ==================
            Simulation with pheromone based navigation
            First, prime the map, then let the ant free
            ================== """
        pheromone = self.Dom.get_pheromone_level([self.Ant.sensors['left'],
                                                  self.Ant.sensors['right']],
                                                 islist= True)
        print(pheromone)


class MultiSim():
    """ ==================
        Do a simulation of a system of Ants
        ================== """
    def __init__(self, size = [1000,1000], pitch = 1, n_ants = 10):
        """ ==================
            Do a simulation of an Ant
            ================== """
        self.size = size
        self.pitch = pitch

        self.Dom = AntDomain(size, pitch)
        self.Dom.set_gaussian(sigma = 25)
        self.Ants = QueenAnt(Ant(limits = size, start_pos = np.dot(0.5,size), speed=10, v_max =20))
        self.Plot = MapPlot(self.Dom.Map.X,self.Dom.Map.Y)


def runSimpleSim():
    S = SimpleSim()
    S.random_roll_sim()

if __name__ == '__main__':
    runSimpleSim()
