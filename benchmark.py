from record_and_play import record_and_play as run_func
import numpy as np
from time import time

dt = .3
steps = 2000
sens_dict = {
    'breakpoint': .25,
    'exp_lambda': 4.
}
ant_dict = {
    'l': 50.,
    'd':25.,
    'sens_offset': 45.,
    'gain': .75,
    'noise_gain': .5,
    'noise_gain2': .1,
    'rotate_fun': 'weber',
    'sens_fun': 'ReLu',
    'sens_dict': sens_dict,
    'deposit_fun': 'exp_decay',
    'steer_regularization': 0.01,
    'override_time': 5.,
    'override_max': .3,
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

n_runs = 10
score_vec = []
initializer = 'BENCHMARK'
comment = 'SIM_1_WEBER_override_v2'
for i in range(n_runs):
    R = run_func(sim_dict, queen_dict, domain_dict,
                 deposit_dict, gauss_dict, record = True, visualize = False,
                 initializer = initializer, comment = comment)
    score_vec.append(R['score'])
    print(f"Sim {R['sim_id']} has an efficiency score of {R['score']}")

print(f"""Mean of the score: {np.mean(score_vec)}
      variance: {np.var(score_vec)}
      min - max: {np.min(score_vec)} - {np.max(score_vec)}""")
