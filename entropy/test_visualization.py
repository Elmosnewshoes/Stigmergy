from core.domain import Domain
from core.visualization import Plotter
from core.plugins.helper_classes import point
import numpy as np

D = Domain([1000,1000], 1)
D.Gaussian = D.init_gaussian(sigma=50)
D.local_add_pheromone(point(*[500,500]),10000)

P = Plotter(D.Map, colormap = 'plasma')
P.draw_stigmergy(D.Map.map)
t = np.arange(-3,3,0.05)
z = 1/(1+np.exp(-t))
P.draw_entropy(z,t=t)
P.set_subtitles()
P.set_labels()
P.show()
