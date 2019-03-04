from cythonic.map_wrapper import MMap, print_I
import numpy as np
import sys
sys.path.append('/home/bram/ANTS/entropy')
from entropy.core.plugins.helper_classes import MeshMap, loc

# M = MMap(dim = np.array([10,10],dtype=np.float_),resolution = .25)
M = MMap(resolution =1,dim = np.array([10,10],dtype=np.float_))
print(M.lim)
print(np.array(M.map).shape)
print(np.array(M.mesh_x).shape)
print(np.array(M.mesh_x))
M2 = MeshMap(dim = [10,10], resolution = 1)

vec = np.array([2,5],dtype = np.float_)


print(M.get_bounds(vec,1))
print(M2.span(loc(*vec),1))
