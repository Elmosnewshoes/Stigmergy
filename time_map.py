from cythonic.map_wrapper import MMap, print_I
import numpy as np
import sys
sys.path.append('/home/bram/ANTS/entropy')
from entropy.core.plugins.helper_classes import MeshMap, loc

# M = MMap(dim = np.array([10,10],dtype=np.float_),resolution = .25)
M = MMap(resolution =.25, R = 5., covariance = 2.)
print(M.rounded(1))
print(M.lim)
print(np.array(M.map).shape)
print(np.array(M.mesh_x).shape)
print(np.array(M.mesh_x))
M2 = MeshMap(dim = [10,10], resolution = .25)

vec = [40,5]
print(M.get_bounds(vec,1))
print(M2.span(loc(*vec),1))
