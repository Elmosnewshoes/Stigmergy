import numpy as np
from time import time as t
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def gaussian(X,Y, mu, sig):
    """ ==============================
        calculate the value of a 2D NORMALIZED gaussian function
        e.g.: Volume of f(x,y)==1
        ============================== """
    A = sig*sig*2*np.pi
    G = np.exp(-np.add(np.power(X-mu[0],2)/(2*np.power(sig,2)),np.power(Y-mu[1],2)/(2*np.power(sig,2))))

    return G/A #np.divide(1,A)*G


dx = 0.1
x = np.arange(-5,5,dx)
y = np.arange(-5,5,dx)
X,Y = np.meshgrid(x,y)
Z =[]
tic = t()
iters = 0
for ii in np.arange(-2,2,0.1):
    Z.append(gaussian(X,Y,(ii,ii),sig=.3))
    iters+=1
print("{} iterations took {}s".format(iters,t()-tic))

ZZ = np.sum(Z,axis=0)

print("Grid size = {} pixels".format(ZZ.size))

fig = plt.figure()
ax = fig.add_subplot(111)
surf = plt.imshow(ZZ, interpolation='bilinear', origin='lower',
                cmap=cm.gray_r, extent=(-5,5,-5,5))
plt.title('simple contour plot')
plt.show()
