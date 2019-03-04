# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Standalone file used to record an theANT3000 simulation
# =======================================
from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict
print(sim_dict)
print(domain_dict)
print(ant_dict)

sim_dict['steps'] = 1000
domain_dict['pitch']=2

from cythonic.sim_wrapper import recorder
sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict)
result = sim_recorder.time_full_sim(record = True, deposit_style = 'constant', deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = 500)
print(result)
