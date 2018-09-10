import numpy as np
x = np.matrix([[-1,2],[3,-4]])
print(np.where(x<0,0,x))
print(np.minimum([-6,2],[1,-0]))
print(type(x))
print(type(x)==np.matrix)
