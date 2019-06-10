from cythonic.plugins.db_path import db_path
path = db_path()+'maps/'

import numpy as np
import matplotlib.image as mpimg
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.markers as markers
from cythonic.plugins.db_controller import db_controller
from math import ceil

# id = 6108
id = 5975

db = db_controller(db_path(),'stigmergy.db')
qry = f"""select id, scorecard,step_vec,entropy_vec, size, nest_loc,food_loc,food_rad, pheromone_max from
sim
left join domain_settings d on d.sim_id = sim.id
left join results on results.sim_id = sim.id
where sim.id = {id} and sim.status= 'FINISHED'"""
db_result = db.return_all(qry)
db.close()
result = {}
for i in range(len(db_result[1])):
    result[db_result[1][i]] = db_result[0][0][i]

iter = 1000
dt = .3

img_name = f'{id}_i{iter}.npy'

x_nest,y_nest = eval(result['nest_loc'])
x_food,y_food = eval(result['food_loc'])
size = eval(result['size'])
r = result['food_rad']
vmax = ceil(result['pheromone_max']/5)*5

map = np.load(path+img_name)
cmaps = {'blue': 'PuBu',
         'grey_reverse': 'Greys_r',
         'grey': 'Greys',
         'plasma': 'plasma'
         }
colormap = 'blue'

opts = {'cmap':plt.get_cmap(cmaps[colormap]),
                       'extent':[0,size[0],
                                 0,size[1]],
                       'vmin':0,'vmax':vmax,
                       'origin':'bottom'}
plt.subplot(111)
img = plt.imshow(map,interpolation="bicubic",**opts)
# plt.colorbar(orientation ='horizontal', label='pheromone level')
scat =plt.plot([x_nest,x_food],[y_nest,y_food], 'o', mfc='none', markersize=50, color = 'k')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
# plt.title(f'Pheromone distribution at t = {int(iter*dt)} sec')
plt.show()

# plt.subplot(111)
# line = plt.plot(np.array(eval(result['step_vec']))*dt,eval(result['scorecard']), color='black')
# plt.xlabel('t [s]')
# plt.ylabel('returned agents [-]')
# plt.title('Evolution of the score')
# plt.show()

# plt.subplot(111)
# line = plt.plot(np.array(eval(result['step_vec']))*dt,eval(result['entropy_vec']), color='black')
# plt.ylim([9,15])
# plt.xlabel('t [s]')
# plt.ylabel('Shannon entropy [-]')
# plt.title('Evolution of the entropy of the pheromone map')
# plt.show()
