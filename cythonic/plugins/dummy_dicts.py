dt = .3
steps = 1000
sens_dict = {
    # 'gain': 1.,
    'breakpoint': 1.,
    # 'snr': 0.1,
    'exp_lambda': 4.
}
ant_dict = {
    'l': 50.,
    'd':50.,
    'sens_offset': 45.,
    'gain': .1,
    'noise_gain': 1.,
    'noise_gain2': 1.,
    'rotate_fun': 'simple',
    'sens_fun': 'linear',
    'sens_dict': sens_dict,
    'deposit_fun': 'exp_decay',
    'steer_regularization': 0.001,
    'override_time': 1.,
    'override_max': 0.,
    'override': 'FALSE'
}

queen_dict = {
    'ant_dict': ant_dict,
    'default_speed': 125.,
    'noise_type': 'telegraph', # can use uniform/white/telegraph
    'noise_parameter': .5,
}

domain_dict = {
    'size': [3000,2000],
    'pitch': 10,
    'nest_loc': [500,1000],
    'nest_rad': 150,
    'food_loc': [2500,1000],
    'food_rad': 150,
    'target_pheromone': 1.
}

gauss_dict = {
    'significancy': 1e2,
    'covariance': 15.
}

sim_dict = {
    'n_agents': 80,
    'dt': dt,
    'steps': steps,
    'deploy_style': 'nest_radian',
    'deploy_timing': 'gamma_dist',
    'deploy_timing_args': {'k':10.,'teta': 2., 't_max': 10},
    'evap_rate': -1.
    # 'evap_rate': 0.99,
}

deposit_dict = {
        'q': 1.,
        'return_factor': 1.,
        'beta':.05 #lambda in Q(t) = Q(0)*exp(-lambda*t) with lambda is protected name
}
