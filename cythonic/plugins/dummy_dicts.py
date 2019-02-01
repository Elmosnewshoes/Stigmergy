dt = .5
steps = 1000
ant_dict = {
    'l': 5.,
    'sens_offset': 45.,
    'gain': 1.,
    'sens_fun': 'linear',
}

queen_dict = {
    # 'dt': dt,
    'ant_dict': ant_dict,
    'default_speed': 5.,
    'noise_type': 'white', # can use uniform/white/telegraph
    'noise_parameter': 2.,
    # 'total_steps': steps
}

domain_dict = {
    'size': [1000,1000],
    'pitch': .5,
    'nest_loc': [250,500],
    'nest_rad': 50,
    'food_loc': [750,500],
    'food_rad': 50,
    'target_pheromone': 1e6
}

gauss_dict = {
    'significancy': 1e2,
    'covariance': 15.
}

sim_dict = {
    'n_agents': 10,
    'dt': dt,
    'steps': steps,
    'deploy_style': 'nest_radian',
    'deploy_timing': 'gamma_dist',
    'deploy_timing_args': {'k':4.,'teta': 2.},
    'evap_rate': -1.
}

deposit_dict = {
        'q': 1.,
        'return_factor': 1,
        'beta':.2
}
sens_dict = {
    'gain': 1.,
    'breakpoint': 1.,
    'snr': 0.1,
    'exp_lambda': 4
}
