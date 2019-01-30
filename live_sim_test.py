from cythonic.core.simulation import live_sim
from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict

sim_dict['steps'] = 100
domain_dict['pitch'] = 2
print(domain_dict)


simulator = live_sim(queen_args = queen_dict, domain_args=domain_dict, sim_args = sim_dict)

simulator.setup_sim('constant', deposit_dict, gauss_dict, display_interval =5,)

simulator.run_sim(5)
