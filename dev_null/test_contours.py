import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 0.025

x = np.arange(-30.,30.,delta)
y = np.arange(-20.,20., delta)

X,Y = np.meshgrid(x,y)
print(Y.shape)

tic = time.time()
Z1 = mlab.bivariate_normal(X,Y, 1.,1., -.5,-.5)
print(Z1.shape)
print('Elapsed seconds: {}'.format(time.time()-tic))
Z2 = mlab.bivariate_normal(X,Y,1.5,1.5, .5, .5)
Z = 100*(Z2-Z1)


# do the plotting

plt.figure()
im = plt.imshow(Z, interpolation='bilinear', origin='lower',
                cmap=cm.gray, extent=(-30, 30, -20, 20))
CS=plt.contour(X,Y,Z,10,linewidths=np.arange(.5, 4, .5))
manual_locations = [(-1, -1.4), (-0.62, -0.7), (-2, 0.5), (1.7, 1.2), (2.0, 1.4), (2.4, 1.7)]
plt.clabel(CS,inline=1,fontsize = 10, manual = manual_locations)
plt.title('simple contour plot')



plt.show()
