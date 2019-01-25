ant_dict = {
    'l': 5.,
    'sens_offset': 45.,
    'gain': 1.,
}

ant_state_dict = {
    
}

queen_dict = {
    'dt': .5,
    'ant_dict': ant_dict
}

domain_dict = {
    'size': [1000,1000],
    'pitch': .5,
    'nest_loc': [250,500],
    'nest_rad': 50,
    'food_loc': [750,500],
    'food_rad': 50,
    'target_pheromone': 1.
}

sim_dict = {
    'n_agents': 10,
    'dt': 1.,
    'steps': 1000,
    'deploy_style': 'nest_radian',
    'deploy_timing': 'gamma_dist',
    'deploy_timing_args': {'k':4.,'teta': 2.},

}
deposit_dict = {
        'q': 1.,
        'return_factor': 1,
        'beta':.2
}
