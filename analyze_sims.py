from cythonic.plugins.db_path import db_path
from cythonic.plugins.functions import score
path = db_path()+'maps/'

import numpy as np
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D  #
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.markers as markers
import matplotlib.colors  as colors
from matplotlib import cm
from cythonic.plugins.db_controller import db_controller
from math import ceil

plt.rc('text', usetex=True)
initializer = 'BENCHMARK'

# ==== for simple controller:
# comment = ['SIM_1_SIMPLE_v4','SIM_1_SIMPLE_override_v2','SIM_1_SIMPLE_override_v3']
# labels = ['Exp. \#1: $\eta=0$', 'Exp. \#2: $\eta=0.2$', 'Exp. \#3: $\eta=0.6$']

# ===== for weber controller
# comment = ['SIM_1_WEBER_v6','SIM_1_WEBER_override_v7','SIM_1_WEBER_override_v8','SIM_1_WEBER_override_v9']
# labels = ['Exp. \#1: $\eta=0$', 'Exp. \#2: $\eta=0.1$', 'Exp. \#3: $\eta=0.3$',  'Exp. \#4: $\eta=0.6$']

# ===== for weber evap rate and colony size sweep =====

# comment = ['sweep_weber','sweep_weber_override2']
comment = ['sweep_weber_2','sweep_weber_3']

db = db_controller(db_path(),'stigmergy.db')
qry = f"""
    select
        sim.id,
        cast(substr(nest_loc,2,instr(nest_loc,', ')-1) as numeric) as X1,
        cast(substr(nest_loc,instr(nest_loc,', ')+2,instr(nest_loc,']')-instr(nest_loc,', ')-1) as numeric) as Y1,
        cast(substr(food_loc,2,instr(food_loc,', ')-1) as numeric) as X2,
        cast(substr(food_loc,instr(food_loc,', ')+2,instr(food_loc,']')-instr(food_loc,', ')-1) as numeric) as Y2,
        dom.food_rad, dom.nest_rad,
        cast(sim_s.steps as numeric) * sim_s.dt as T,
        sim_s.dt as dt,
        sim_s.n_agents as N,
        sim.comment,
        queen.default_speed as S,
        results.nestcount as nestcount,
        results.step_vec as step_vec,
        results.scorecard,
        sim.steps_recorded,
        sim_s.evap_rate
    from sim
    left join domain_settings dom on dom.sim_id = sim.id
    left join sim_settings as sim_s on sim_s.sim_id = sim.id
    left join queen_settings as queen on queen.sim_id = sim.id
    left join results on results.sim_id = sim.id
    where
        dom.sim_id is not null
        AND sim.status= 'FINISHED' and sim.comment in ({"'"+"','".join(comment)+"'"}) and sim.initializer = '{initializer}'
        AND sim_s.sim_id is not null
        AND queen.sim_id is not null
        AND queen.default_speed is not null
        AND sim_s.dt is not null
        AND sim_s.steps is not null
        AND results.sim_id is not null
        AND results.nestcount is not null
        AND steps_recorded is not null"""

df = db.get_df(qry)
df['DX'] = df['X1']-df['X2']
df['DY'] = df['Y1']-df['Y2']
df['R'] = np.sqrt(df['DX']**2+df['DY']**2)
df['score'] = 2*df['nestcount'] * df['R'] / (df['steps_recorded']*df['dt'] * df['S'])



N = df['N'].to_numpy()
rho = df['evap_rate'].to_numpy()
Upsilon = df['score'].to_numpy()

n_map =sorted(list(set(N)))
rho_map = sorted(list(set(rho)))



fig = plt.figure()
ax = fig.gca()
x = [5, 10, 25]
y = [.3,.4,.5]

n_v, rho_v = np.meshgrid(n_map, rho_map,)
z = np.zeros(n_v.shape)
for i in range(len(Upsilon)):
    z[(n_v ==N[i]) & (rho_v == rho[i])]+=Upsilon[i]
z *=1/(len(Upsilon)/z.size)
t_v = np.log(.5)/np.log(rho_v)

print(t_v[:,0].round())
print(n_map)
print(z)
print(f"Number of samples per scenario {len(Upsilon)/z.size}")

print(z[(n_v ==120) & (t_v.round()==5)  ])

# Make data.
# Plot the surface.
# print(df['score'].to_numpy())
# surf = ax.plot_surface(n_v, t_v, z, cmap = cm.get_cmap("PuBu"), antialiased=True)
surf = ax.imshow( z, interpolation = 'bicubic',origin='bottom', vmin = 0,vmax = .9, cmap = 'Spectral',norm =colors.PowerNorm(gamma=1. / 1.5))
# Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel('Colony size M [-]')
ax.set_ylabel('$t_{1/2} [s]$')
ax.set_title('Efficiency score analysis')
plt.xticks(np.arange(8), n_map)
plt.yticks(np.arange(7),t_v[:,0].round(0))
# #
plt.show()

#======= surface plot of 2-parameter sweep ======



# ====== Calculate score and final score correlation =====
# R = {'steps': [],
#      'name': [],
#      'score':[],
#      'score_vec': [],
#      'last_score':[],
#      'R': [],
#      'S': [],
#      'N':[]
#      }

# def get_last(row):
#     # returns difference between last entry in list and 11th last entry
#     return row[-1]- row[-11]
#
# for index, row in df.iterrows():
#     R['steps'].append( get_last(eval(row['step_vec']))*0.3)
#     R['score_vec'].append( get_last(eval(row['scorecard']))*0.3)
#     R['name'].append( row['comment'])
#     R['score'].append(row['score'])
#     R['R'].append(row['R'])
#     R['S'].append(row['S'])
#     R['N'].append(row['N'])
#
# for i in range(len(R['score'])):
#     R['last_score'].append(2*R['R'][i]*R['score_vec'][i]/(R['N'][i]*R['S'][i]*R['steps'][i]*0.3))
# print(R['last_score'])
#
# marker = ['o','x','+','d']
# color = ['blue', 'orange','black','green']
# fig, ax = plt.subplots()
# for i in range(4):
#     ax.scatter(R['score'][i*100:(i+1)*100], R['last_score'][i*100:(i+1)*100],c=color[i],marker= marker[i],label=labels[i])
# ax.plot([0,1.2],[0,1.2], color = 'k', linestyle = '--', label = 'autocorrelation', alpha = .5)
# ax.legend()
# ax.grid(True)
# ax.set_title('Efficieny')
# ax.set_xlabel('Global efficiency [-]')
# ax.set_ylabel('Final efficiency [-]')
# plt.show()

# ===== sim properties ======
# for sim in comment:
#     mu = df.loc[df['comment']==sim]['score'].mean()
#     min = df.loc[df['comment']==sim]['score'].min()
#     max = df.loc[df['comment']==sim]['score'].max()
#     var = df.loc[df['comment']==sim]['score'].var()
#     print(f"Experiment {sim} has avg score: {round(mu,3)}, with variance {round(var,5)} and max-min {round(max,3)} - {round(min,3)}")
#
# fig, ax = plt.subplots()
# ax.set_title('Simulation results with a weber\'s control law')
# ax.boxplot([df.loc[df['comment']==comment[i]]['score'] for i in range(len(comment))],
#             notch=True,
#             labels = labels)
# ax.set_ylabel('Efficiency [-]')
# plt.show()
