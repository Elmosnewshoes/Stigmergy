# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Standalone file used to record and then play an theANT3000 simulation
# =======================================
from animate_sim import show_plot
from cythonic.sim_wrapper import recorder
import cProfile, pstats

def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            ps = pstats.Stats(profile).sort_stats('cumulative')
            ps.print_stats()
    return profiled_func


def record_and_play(sim_dict, queen_dict, domain_dict, deposit_dict, gauss_dict, record, upload_interval = 500, visualize = True, **kwargs):
    sim_recorder = recorder(queen_args = queen_dict, domain_args = domain_dict, sim_args = sim_dict, **kwargs)
    result = sim_recorder.time_full_sim(record = record, deposit_dict = deposit_dict,gauss_dict = gauss_dict, upload_interval = upload_interval)
    if record and visualize:
        animation = show_plot(result['sim_id'], colormap = 'blue')
    elif visualize:
        pass
    return result

@do_cprofile
def profiled_run(*args, **kwargs):
    return run()

def run(*args,**kwargs):
    result = record_and_play(sim_dict,queen_dict,domain_dict, deposit_dict,gauss_dict, record, 500, visualize)
    print(f"Sim {result['sim_id']} has an efficiency score of {result['score']}")

if __name__ == '__main__':
    from cythonic.plugins.dummy_dicts import ant_dict, queen_dict, domain_dict, gauss_dict, sim_dict, deposit_dict, sens_dict
    # domain_dict = {
    #     'size': [2000,1500],
    #     'pitch': 5,
    #     'nest_loc': [250,750],
    #     'nest_rad': 150,
    #     'food_loc': [1750,750],
    #     'food_rad': 150,
    #     'target_pheromone': 1.
    # }
    # sim_dict['steps'] = 3000
    # sim_dict['dt'] = .3
    # sim_dict['n_agents'] = 80
    # queen_dict['default_speed'] = 125
    # sim_dict['evap_rate'] = .97
    # queen_dict['noise_type'] = 'white'
    # queen_dict['noise_parameter'] = 10 #higher means direction changes last longer with telegraph noise
    # ant_dict['deposit_fun'] = 'exp_decay'
    # deposit_dict['beta'] = .01
    # record = True
    # visualize = False
    #
    # ant_dict['gain'] = 0.5
    # ant_dict['d'] = .1*ant_dict['l']
    # ant_dict['rotate_fun'] = 'weber'
    # ant_dict['noise_gain'] = 0.75
    # ant_dict['noise_gain2'] = 0.05
    # sim_dict['evap_rate'] = 0.97
    # ant_dict['sens_offset'] = 25
    # ant_dict['sens_fun'] = 'ReLu'
    # ant_dict['sens_dict']['breakpoint'] = .5
    # gauss_dict['covariance'] = 400
    # deposit_dict['q'] = 2
    record = True
    visualize = False
    dt = .3
    steps = 2000
    sens_dict = {
        'breakpoint': .25,
        'exp_lambda': 4.
    }
    ant_dict = {
        'l': 50.,
        'd':10.,
        'sens_offset': 25.,
        'gain': .75,
        'noise_gain': .5,
        'noise_gain2': .1,
        'rotate_fun': 'weber',
        'sens_fun': 'ReLu',
        'sens_dict': sens_dict,
        'deposit_fun': 'exp_decay',
        'steer_regularization': 0.01,
        'override_time': 5.,
        'override_max': .1,
        'override': 'TRUE'
    }

    queen_dict = {
        'ant_dict': ant_dict,
        'default_speed': 125.,
        'noise_type': 'white', # can use uniform/white/telegraph
        'noise_parameter': 10,
    }

    domain_dict = {
        'size': [2500,1000],
        'pitch': 10,
        'nest_loc': [500,500],
        'nest_rad': 150,
        'food_loc': [2000,500],
        'food_rad': 150,
        'target_pheromone': 1.
    }

    gauss_dict = {
        'significancy': 1e2,
        'covariance': 200.
    }

    sim_dict = {
        'n_agents': 120,
        'dt': dt,
        'steps': steps,
        'deploy_style': 'nest_radian',
        'deploy_timing': 'gamma_dist',
        'deploy_timing_args': {'k':10.,'teta': 2., 't_max': 111},
        'evap_rate': .97
    }

    deposit_dict = {
            'q': 1.,
            'return_factor': 2.,
            'beta':.03 #lambda in Q(t) = Q(0)*exp(-lambda*t) with lambda is protected name
    }


    profiled_run(sim_dict = sim_dict,
                 queen_dict = queen_dict,
                 deposit_dict = deposit_dict,
                 gauss_dict = gauss_dict,
                 record=record,
                 visualize = visualize)
