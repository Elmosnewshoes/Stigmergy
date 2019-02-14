from animate_sim import show_plot as plotter
from cythonic.sim_wrapper import recorder
from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict

sim_dict['steps'] = 1000
domain_dict['pitch']=10
deposit_dict['q'] = 1000
ant_dict['gain'] = .5
ant_dict['noise_gain']= 10
gauss_dict['covariance']= 15
sim_dict['evap_rate'] = .97
queen_dict['noise_type'] = 'telegraph'
queen_dict['noise_parameter'] = 20
record = False
sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict)
result = sim_recorder.time_full_sim(record = record, deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = 500)
print(result)
if record: plotter(result['sim_id'], colormap = 'blue')
