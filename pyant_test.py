from cythonic.wrapper import cube_wrapped,pnt, sens
print(cube_wrapped(3.0))
print(pnt(3.,5.))
from cythonic.wrapper import pyAnt, rotate
import numpy as np


A = pyAnt(id =1, speed = 10, gain = 2, l = 5, sens_offset = 45,
          limits = np.array([10,10],dtype=np.float_))

print(A.attributes())
print(A.foodbound   )

A.azimuth = 360
print(A.azimuth)

print(pnt(3.,2.))

A.init_positions(np.array([1,1], dtype=np.float_))
print(A.pos)
print(A.chck_bnds())
print(A.return_positions())

print(sens('linear', 10))

#
# print(rotate(30.).dot([1,0]))
# A.init_positions(np.array([0.,0.],dtype=np.float_))
# print(A.pos)
# print(A.left)
# print(A.right)
# A.pos.x = 10.
