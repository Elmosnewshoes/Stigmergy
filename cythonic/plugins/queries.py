"""
    Here are a bunch of queries used for storing simulation parameters into
    the sqlite database
"""

def insert(table):
    return f"INSERT INTO {table} "

def insert_ant(l, sens_offset, gain, noise_gain, sens_fun, **kwargs):
    output = insert('ant_settings') + "(l, sens_offset, gain, noise_gain, sens_fun) "
    output += f" VALUES ({l}, {sens_offset}, {gain}, {noise_gain}, '{sens_fun}')"
    return output

def insert_queen(default_speed, noise_type, noise_parameter, **kwargs):
    output = insert('queen_settings') + "(default_speed, noise_type, noise_parameter) "
    output+= f"VALUES ({default_speed}, '{noise_type}', {noise_parameter})"
    return output

def insert_domain(size, pitch, nest_loc, nest_rad, food_loc, food_rad, target_pheromone, **kwargs):
    output = insert('domain_settings') + "(size, pitch, nest_loc, nest_rad, food_loc, food_rad, target_pheromone) "
    output+= f"VALUES ('{size}', {pitch}, '{nest_loc}', {nest_rad}, '{food_loc}', {food_rad}, {target_pheromone})"
    return output

def insert_gauss(significancy, covariance, **kwargs):
    output = insert('gauss_settings') + "(significancy, covariance) "
    output+= f"VALUES ({significancy}, {covariance})"
    return output

def insert_deposit(q, return_factor, beta, **kwargs):
    output = insert('deposit_settings') + "(q, return_factor, beta) "
    output+= f"VALUES ({q}, {return_factor}, {beta})"
    return output

def insert_results(entropy_vec = 'NULL', start_entropy = 'NULL',end_entropy = 'NULL',
                   foodcount = 'NULL', nestcount = 'NULL', **kwargs):
    if entropy_vec !='NULL':
        # add string identifiers!
        entropy_vec = f"'{entropy_vec}'"
    output = insert('results') + "(entropy_vec, start_entropy, end_entropy, foodcount, nestcount) "
    output+= f"VALUES ({entropy_vec}, {start_entropy}, {end_entropy}, {foodcount}, {nestcount})
    return output

def insert_sens(breakpoint, exp_lambda, **kwargs):
    output = insert('sens_settings') + "(breakpoint,exp_lambda) "
    output+= f"VALUES ({breakpoint},{exp_lambda}) "
    return output

def sim_settings(n_agents, dt, steps, deploy_style, deploy_timing, deploy_timing_args, evap_rate, **kwargs):
    output = insert('sim_settings') + "(n_agents, dt, steps, deploy_style, deploy_timing, deploy_timing_args, evap_rate) "
    output+= f"VALUES ({n_agents}, {dt}, {steps}, '{deploy_style}', '{deploy_timing}', '{deploy_timing_args}', {evap_rate}) "
    return output

from dummy_dicts import ant_dict, queen_dict, domain_dict
print(insert_queen(**queen_dict))
print(insert_domain(**domain_dict))
