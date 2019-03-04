# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Standalone file used to record and then play an theANT3000 simulation
# =======================================
from animate_sim import show_plot
from cythonic.sim_wrapper import recorder


def record_and_play(sim_dict, queen_dict, domain_dict, deposit_dict, gauss_dict, record, upload_interval = 500, visualize = True):
    sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict)
    result = sim_recorder.time_full_sim(record = record, deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = upload_interval)
    if record and visualize:
        animation = show_plot(result['sim_id'], colormap = 'blue')

if __name__ == '__main__':
    from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict

    domain_dict = {
        'size': [2000,1500],
        'pitch': 10,
        'nest_loc': [500,750],
        'nest_rad': 150,
        'food_loc': [1500,750],
        'food_rad': 150,
        'target_pheromone': 1.
    }
    sim_dict['steps'] = 2000
    sim_dict['n_agents'] = 80
    domain_dict['pitch']=10
    queen_dict['default_speed'] = 125
    sim_dict['evap_rate'] = .97
    queen_dict['noise_type'] = 'telegraph'
    queen_dict['noise_parameter'] = 10 #higher means direction changes last longer with telegraph noise
    ant_dict['deposit_fun'] = 'exp_decay'
    deposit_dict['beta'] = .01
    record = True
    visualize = True

    ant_dict['gain'] = 0.5
    ant_dict['noise_gain'] = 0.75
    sim_dict['evap_rate'] = 0.97
    ant_dict['sens_offset'] = 45
    deposit_dict['covariance'] = 35
    deposit_dict['q'] = 1500 # originally 1000
    record_and_play(sim_dict,queen_dict,domain_dict, deposit_dict,gauss_dict, record, 500, visualize)
