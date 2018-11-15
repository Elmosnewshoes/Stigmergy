create_new_sim = """
    INSERT INTO sims(n_agents,dt,target_pheromone_volume,
    pheromone_variance,deploy_method,deploy_location,sens_function)
VALUES ({n_agents},{dt},{target_pheromone_volume},{sigma},
    '{deploy_method}', '{deploy_location}','{sens_function}') """

insert_ant_settings = """
    INSERT INTO ant_settings (sim_id,speed,l, antenna_offset, limits,drop_quantity,
    gain,beta, noise_gain,drop_fun,return_factor) VALUES (
    {sim_id}, {speed}, {l},{antenna_offset},'{limits}',{drop_quantity},{gain},{beta},{noise_gain},
    '{drop_fun}',{return_factor}) """

insert_domain_settings = """
    INSERT INTO domain_settings (sim_id, size,nest_location, nest_radius,
    food_location,food_radius, pitch) VALUES
    ({sim_id},'{size}','{nest_location}',{nest_radius},'{food_location}',{food_radius},
    {pitch}) """

insert_results = """ INSERT INTO results (sim_id, start_entropy, end_entropy, entropy_vec, time_vec, foodcount, returncount,image_path)
    VALUES ({sim_id}, {start_entropy}, {end_entropy},'{entropy_vec}','{time_vec}',{foodcount},{returncount},'{image_path}')
    """

# insert_step = {'qry': "INSERT INTO sim_updates(STEP,SIM_ID) VALUES {args}",
#                'args': '({step},{sim_id}),'}

insert_stepupdates = {'qry': """INSERT INTO ant_updates(SIM_ID, STEP,ANT_ID, X,Y,TETA,Q)
                      VALUES {args}""",
                      'args': '({sim_id},{step},{ant_id},{x},{y},{teta},{Q}),'}

get_antcount = """SELECT n_agents FROM sims as sim WHERE sim.id = {id}
    """
get_ant_table = "SELECT * FROM ant_updates WHERE ant_id = {ant_id} AND sim_id ={sim_id}"

get_sim = """SELECT sim.target_pheromone_volume, sim.pheromone_variance,
    dom.size, dom.pitch, dom.nest_location, dom.nest_radius,dom.food_location,dom.food_radius,
    ant.speed, ant.antenna_offset, ant.l, IFNULL(results.entropy_vec,'[]'), IFNULL(results.time_vec,'[]')
    FROM sims AS sim, domain_settings AS dom, ant_settings AS ant
    LEFT JOIN results ON results.sim_id = sim.id
    WHERE sim.id = {id}
    AND sim.id = dom.sim_id
    AND ant.sim_id = sim.id """

get_latest_id = "SELECT max(id) FROM sims"
