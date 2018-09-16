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


    def draw_ant_scatter(self):
        self.Plot.draw_scatter(self.Ant.pos.x, self.Ant.pos.y)
        self.Plot.draw_scatter(self.Ant.sensors['left'].x, self.Ant.sensors['left'].y, marker = 'o', name = 'sensor_left')
        self.Plot.draw_scatter(self.Ant.sensors['right'].x, self.Ant.sensors['right'].y, marker = 'o', name = 'sensor_right')

    def random_roll_sim(self,n_steps = 500, contour_interval = 1):
        """ ==================
            Simulation the pheromone accumulation with random steps
            ================== """
        # == Start loop ==
        for i in range(n_steps):
            self.Ant.random_roll(sigma_speed = 5, sigma_rotate = 0.1) # do random step
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
        self.Ant.v =self.Ant.v /5
        for i in range(50):
            loc = self.size*np.random.rand(1,2)[0]
            self.Dom.add_pheromone(Q =0.25,sigma = 50,loc=loc,peak_1=True)
        self.Dom.update_pheromone()
        self.Plot.draw_contour(self.Dom.Map.map)

        # == loop over the simulation ==
        for i in range(n_steps):
            pheromone = self.Dom.get_pheromone_level(self.Ant.sens_loc,
                                                     islist=True)
            self.Ant.gradient_step([self.Ant.observed_pheromone(pheromone[0],activation = 'linear'),
                                    self.Ant.observed_pheromone(pheromone[1],activation = 'linear')],
                                   gain = 0.025,
                                   SNR = 0.05)
            self.Dom.local_add_pheromone(self.Ant.pos.vec, peak_1 = True, Q = 0.1) # add pheromone to the map
            self.Dom.update_pheromone() # update the global map
            self.draw_ant_scatter()

            if i%contour_interval ==0:
                print("At step {:d}".format(i))
                self.Plot.draw_contour(self.Dom.Map.map)


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
    # S.random_roll_sim()
    S.gradient_sim(contour_interval = 10, n_steps = 1500)
    # ==All done, lock the graph ==
    S.Plot.hold_until_close()
if __name__ == '__main__':
    runSimpleSim()
