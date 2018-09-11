import numpy as np
import small_functions as fun
x = np.matrix([[-1,2],[3,-4]])
print(np.where(x<0,0,x))
print(np.minimum([-6,2],[1,-0]))
print(type(x))
print(type(x)==np.matrix)
P = fun.Point([1,1])
print(type(P)==fun.Point)
print(fun.Point)
print(type(fun.Point)
