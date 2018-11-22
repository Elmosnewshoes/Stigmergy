from cythonic.wrapper import cube_wrapped,pnt, sens
print(cube_wrapped(3.0))
print(pnt(3.,5.))
from cythonic.wrapper import pyAnt, rotate
import numpy as np


A = pyAnt(id =1, speed = 10, gain = 2, l = 5, sens_offset = 45,
          limits = np.array([10,10],dtype=np.float_),q = 1.5, return_factor = 1,
          drop_fun = 'exp_decay', drop_beta = .5)

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
print(A.return_observed('linear', [1.,2.]))
print(A.return_drop_quantity())
A.gradient_step(.5)
print(A.time)
print(A.return_drop_quantity())

n = 1e5

t_observe = A.time_observe(n)
t_step = A.time_step(n)
t_sensors  = A.time_sensors(n)
t_full = A.time_iteration(n)
print("Observe took avg {} msec ".format(A.time_observe(n)/n))
print("Step took avg {} msec ".format(t_step/n))
print("Set sensors took avg {} msec".format(t_sensors/n))
print("Full ant iteration took avg {} msec".format(t_full/n))
