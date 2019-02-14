from animate_sim import show_plot as plotter
from cythonic.sim_wrapper import recorder
from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict

sim_dict['steps'] = 1000
domain_dict['pitch']=10
deposit_dict['q'] = 1000
ant_dict['gain'] = .05
ant_dict['noise_gain']= 20
gauss_dict['covariance']= 15
sim_dict['evap_rate'] = .97
queen_dict['noise_type'] = 'telegraph'
queen_dict['noise_parameter'] = 5
sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict)
result = sim_recorder.time_full_sim(record = True, deposit_style = 'constant', deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = 500)
print(result)
plotter(result['sim_id'], colormap = 'blue')
