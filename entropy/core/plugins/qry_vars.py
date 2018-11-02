create_new_sim = """
    INSERT INTO sims(n_agents,domain_limits,pitch,dt,
nest_location,nest_radius,food_location,food_radius,
start_concentration,pheromone_variance,
deploy_method,deploy_location,
sens_function, ant_start_speed, ant_antenna_offset,ant_l)
VALUES ({n_agents},'{limits}',{pitch},{dt},
    '{nest_location}',{nest_radius},'{food_location}',{food_radius},
    {start_concentration},{sigma},
    '{deploy_method}', '{deploy_location}',
    '{sens_function}', {speed}, {antenna_offset}, {l})"""

insert_step = {'qry': "INSERT INTO sim_updates(STEP,SIM_ID) VALUES {args}",
               'args': '({step},{sim_id}),'}

insert_stepupdates = {'qry': """INSERT INTO ant_updates(STEP_ID,ANT_ID, X,Y,TETA,Q)
                      VALUES {args}""",
                      'args': '({step},{ant_id},{x},{y},{teta},{Q}),'}
