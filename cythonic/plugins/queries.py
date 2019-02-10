"""
    Here are a bunch of queries used for storing simulation parameters into
    the sqlite database
"""

def insert(table):
    return f"INSERT INTO {table} "

def insert_ant(sim_id, l, sens_offset, gain, noise_gain, sens_fun, **kwargs):
    output = insert('ant_settings') + "(sim_id, l, sens_offset, gain, noise_gain, sens_fun) "
    output += f" VALUES ({sim_id}, {l}, {sens_offset}, {gain}, {noise_gain}, '{sens_fun}')"
    return output

def insert_queen(sim_id, default_speed, noise_type, noise_parameter, **kwargs):
    output = insert('queen_settings') + "(sim_id, default_speed, noise_type, noise_parameter) "
    output+= f"VALUES ({sim_id}, {default_speed}, '{noise_type}', {noise_parameter})"
    return output

def insert_domain(sim_id, size, pitch, nest_loc, nest_rad, food_loc, food_rad, target_pheromone, **kwargs):
    output = insert('domain_settings') + "(sim_id, size, pitch, nest_loc, nest_rad, food_loc, food_rad, target_pheromone) "
    output+= f"VALUES ({sim_id}, '{size}', {pitch}, '{nest_loc}', {nest_rad}, '{food_loc}', {food_rad}, {target_pheromone})"
    return output

def insert_gauss(sim_id, significancy, covariance, **kwargs):
    output = insert('gauss_settings') + "(sim_id, significancy, covariance) "
    output+= f"VALUES ({sim_id}, {significancy}, {covariance})"
    return output

def insert_deposit(sim_id, q, return_factor, beta, **kwargs):
    output = insert('deposit_settings') + "(sim_id, q, return_factor, beta) "
    output+= f"VALUES ({sim_id}, {q}, {return_factor}, {beta})"
    return output

def insert_results(sim_id, entropy_vec = 'NULL', start_entropy = 'NULL',end_entropy = 'NULL',
                   foodcount = 'NULL', nestcount = 'NULL',scorecard='NULL',step_vec='NULL', **kwargs):
    if entropy_vec !='NULL':
        # add string identifiers!
        entropy_vec = f"'{entropy_vec}'"
    if scorecard !='NULL':
        scorecard = f"'{scorecard}'"
    if step_vec  !='NULL':
        step_vec = f"'{step_vec}'"
    output = insert('results') + "(sim_id, entropy_vec, start_entropy, end_entropy, foodcount, nestcount, scorecard) "
    output+= f"VALUES ({sim_id}, {entropy_vec}, {start_entropy}, {end_entropy}, {foodcount}, {nestcount},{scorecard})"
    return output

def insert_sens(sim_id, breakpoint, exp_lambda, **kwargs):
    output = insert('sens_settings') + "(sim_id, breakpoint,exp_lambda) "
    output+= f"VALUES ({sim_id}, {breakpoint},{exp_lambda}) "
    return output

def sim_settings(sim_id, n_agents, dt, steps, deploy_style, deploy_timing, deploy_timing_args, evap_rate, **kwargs):
    output = insert('sim_settings') + "(sim_id, n_agents, dt, steps, deploy_style, deploy_timing, deploy_timing_args, evap_rate) "
    output+= f"VALUES ({sim_id}, {n_agents}, {dt}, {steps}, '{deploy_style}', '{deploy_timing}', '{deploy_timing_args}', {evap_rate}) "
    return output

def new_sim():
    return insert("SIM") + " DEFAULT VALUES "

def insert_stepupdates():
    return "INSERT INTO STEP (SIM_ID, STEP_NR, ANT_ID, X, Y, THETA, Q) VALUES {VALUES}"

def update_sim(sim_id, status = 'STARTED', steps = 'NULL'):
    return f"UPDATE SIM SET STATUS = '{status}', steps_recorded = {steps} WHERE ID = {sim_id} "

def get_settings(sim_id, table):
    return f"SELECT * FROM {table} WHERE {table}.sim_id = {sim_id}"

if __name__ == '__main__':
    from dummy_dicts import ant_dict, queen_dict, domain_dict
    print(insert_queen(1, **queen_dict))
    print(insert_domain(1, **domain_dict))
