create_new_sim = """
    INSERT INTO sims(n_agents,domain_limits,pitch,dt,
nest_location,nest_radius,food_location,food_radius,
target_pheromone_volume,pheromone_variance,
deploy_method,deploy_location,
sens_function, ant_start_speed, ant_antenna_offset,ant_l)
VALUES ({n_agents},'{limits}',{pitch},{dt},
    '{nest_location}',{nest_radius},'{food_location}',{food_radius},
    {target_pheromone_volume},{sigma},
    '{deploy_method}', '{deploy_location}',
    '{sens_function}', {speed}, {antenna_offset}, {l})"""

# insert_step = {'qry': "INSERT INTO sim_updates(STEP,SIM_ID) VALUES {args}",
#                'args': '({step},{sim_id}),'}

insert_stepupdates = {'qry': """INSERT INTO ant_updates(SIM_ID, STEP,ANT_ID, X,Y,TETA,Q)
                      VALUES {args}""",
                      'args': '({sim_id},{step},{ant_id},{x},{y},{teta},{Q}),'}

get_antcount = """SELECT n_agents FROM sims as sim WHERE sim.id = {id}
    """
get_ant_table = "SELECT * FROM ant_updates WHERE ant_id = {ant_id} AND sim_id ={sim_id}"

get_sim = "SELECT * FROM sims WHERE id = {id}"
