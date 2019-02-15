from animate_sim import SubplotAnimation as plotter
import matplotlib.pyplot as plt
from cythonic.sim_wrapper import recorder
from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict

sim_dict['steps'] = 1000
sim_dict['n_agents'] = 80
domain_dict['pitch']=10
deposit_dict['q'] = 1500#1000
ant_dict['gain'] = 0.75#.5
ant_dict['noise_gain']= .5#2
gauss_dict['covariance']= 20
queen_dict['default_speed'] = 125
sim_dict['evap_rate'] = .97
queen_dict['noise_type'] = 'telegraph'
queen_dict['noise_parameter'] = 10 #higher means direction changes last longer with telegraph noise
ant_dict['deposit_fun'] = 'exp_decay'
deposit_dict['beta'] = .01
record = True
sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict)
result = sim_recorder.time_full_sim(record = record, deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = 500)
print(result)
if record:
    animation = plotter(result['sim_id'], colormap = 'blue')
    plt.show()
    print(f'Max of pheromone map: {animation.player.max}')
