import ant
import domain
import plot
from time import *
import numpy as np

pitch = 0.25 #stepsize [mm]
domain_size = (100,100) # in [mm]
steps = 100

# initialize the domain
D = domain.AntDomain(size = domain_size, pitch = pitch)

# initialize the plot based on the domain
P = plot.MapPlot(D.X,D.Y,D.pheromone_map, area_dims = domain_size)
P.set_plot(D.pheromone_map)

xyz = ant.Ant(limits = domain_size,start_pos=(np.random.rand()*domain_size[0],np.random.rand()*domain_size[1]))

# deploy a number of ants
I = 10
Ants = []
for i in range(I):
    start_pos = (0.25*domain_size[0]+0.5*np.random.rand()*domain_size[0],
                 0.25*domain_size[1]+0.5*np.random.rand()*domain_size[1])
    Ants.append(ant.Ant(ant_id=i,limits = domain_size,start_pos=start_pos) )



for i in range(steps):
    print(i)
    # do random walks
    pheromone = []
    x = []
    y=[]
    D.evaporate(xsi=0.9)
    for Ant in Ants:
        Ant.random_step(sigma=1)
        x.append(Ant.x)
        y.append(Ant.y)
        D.add_pheromone(loc = (Ant.x,Ant.y),sigma = 2, Q=10)

    if i%5 == 0:
        draw_bg = True
    else:
        draw_bg = False
    D.update_pheromone()
    P.draw(surf = D.pheromone_map, scat_X=x, scat_Y = y, draw_bg=draw_bg)

    sleep(0.1)
P.hold_until_close()
