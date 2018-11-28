from core.ant import Ant
import numpy as np


ant_settings = {'start_pos': [10,10],
                'angle': 45,
                'speed': 10,
                'limits': [1000,1000],
                'l': 10,
                'antenna_offset': 30,
                'drop_quantity':1,
                'beta':1,
                'noise_gain':1e-3*2*1.75,
                'gain':5,}

ant = Ant(**ant_settings)
rand = []
for _ in range(10000):
    rand.append(ant.rng.exp_signed_rand())
print(np.mean(rand))
