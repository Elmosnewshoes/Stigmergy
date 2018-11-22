from cythonic.map_wrapper import MMap
import numpy as np


M = MMap(dim = np.array([10,10],dtype=np.float_),resolution = .25)
print(M.rounded(1))
print(M.lim)
print(np.array(M.map).shape)
