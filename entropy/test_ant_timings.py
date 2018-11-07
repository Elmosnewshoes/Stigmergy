from core.ant import Ant
from core.plugins.helper_functions import lin_fun
import numpy as np

ant_settings = {'start_pos': [10,10],
                'angle': 45,
                'speed': 10,
                'limits': [1000,1000],
                'l': 10,
                'antenna_offset': 30,
                'drop_quantity':1,
                'noise_gain':1,
                'beta':1,
                'gain':5}

ant = Ant(**ant_settings)
print(ant.sensors['left'].vec)
print(ant.sensors['right'].vec)
ant.observe_pheromone(lin_fun,[1,1])
print(ant.Qobserved)
ant.gradient_step(dt=1)
print(ant.Qobserved)

def time_it():
    "Time all the steps of the ant class, using time for timit bian a PIA"
    import time
    ant = Ant(**ant_settings)
    n = int(1e5)

    " Observe pheromone "
    tic = time.time()
    for Q in np.random.randn(n,2):
        ant.observe_pheromone(lin_fun,Q)
    toc = time.time()
    print("Observed pheromone in avg {} msec".format(1e3*(toc-tic)/n))

    " Step "
    tic = time.time()
    for _ in range(n):
        ant.step(1)
    toc = time.time()
    print("Stepped in avg {} msec".format(1e3*(toc-tic)/n))

    " Update sensors "
    tic = time.time()
    for _ in range(n):
        ant.set_sensor_position()
    toc = time.time()
    print("Updated sensors in avg {} msec".format(1e3*(toc-tic)/n))


    " Total gradient step "
    tic = time.time()
    for Q in np.random.randn(n,2):
        ant.observe_pheromone(lin_fun,Q)
        ant.gradient_step(dt=1)
    toc = time.time()
    print("Total step took avg {} msec".format(1e3*(toc-tic)/n))
time_it()
