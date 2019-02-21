# store some functions (methods) here to declutter the gui.py file in the main directory

def make_domain_dict(Gui):
    the_dict = {
        'size': [Gui.dom_x_size.value(),Gui.dom_x_size.value()],
        'pitch': Gui.spinbox_pitch.value(),
        'nest_loc': [Gui.nest_x_size.value(), Gui.nest_x_size.value()],
        'nest_rad': Gui.spinbox_nestradius.value(),
        'food_loc': [Gui.food_x_size.value(), Gui.food_x_size.value()],
        'food_rad': Gui.spinbox_foodradius.value(),
        'target_pheromone': Gui.spinbox_pheromone.value()
    }
    return the_dict

def make_ant_dict(Gui):
    " return a filled dictionary with all ant parameters from the gui "
    the_dict = {
        'l': Gui.spinbox_antsize.value(),
        'sens_offset':Gui.spinbox_offset.value(),
        'gain': Gui.spinbox_gain.value(),
        'noise_gain': Gui.spinbox_noisegain.value(),
        'sens_fun':  Gui.combobox_activation.currentText(),
        'sens_dict': {'breakpoint': Gui.spinbox_breakpoint.value(),
                      'exp_lambda': Gui.spinbox_lambda.value()},
        'deposit_fun': Gui.combobox_depfun.currentText()
    }
    if the_dict['deposit_fun'] =='exponential': the_dict['deposit_fun']= 'exp_decay'
    return the_dict

def make_queen_dict(Gui):
    the_dict = {
        'ant_dict': make_ant_dict(Gui),
        'default_speed': Gui.spinbox_speed.value(),
        'noise_type': Gui.combobox_noise.currentText(),
        'noise_parameter': eval(Gui.line_noiseparameter.text())
    }
    return the_dict
def make_sim_dict(Gui):
    the_dict = {
        'n_agents':Gui.spinbox_agents.value(),
        'dt':Gui.spinbox_dt.value(),
        'steps':Gui.spinbox_steps.value(),
        'deploy_style':Gui.combobox_deployment.currentText(),
        'deploy_timing':Gui.combobox_timing.currentText(),
        'deploy_timing_args':{
            'k': Gui.spinbox_deployk.value(),
            'teta': Gui.spinbox_deploytheta.value(),
            't_max': Gui.spinbox_deploytmax.value()
            },
        'evap_rate':Gui.spinbox_evaporation.value(),
    }
    return the_dict

def make_gauss_dict(Gui):
    return {'significancy':10**Gui.spinbox_significancy.value(),
            'covariance':Gui.spinbox_covariance.value()}

def make_deposit_dict(Gui):
    the_dict = {
        'q':Gui.spinbox_q.value(),
        'return_factor':Gui.spinbox_returnfactor.value(),
        'beta':Gui.spinbox_depositbeta.value()
    }
    return the_dict

def simulation_args(Gui):
    "return a dictionary that can be used as **kwargs with all simulation dicts"
    return {
        'sim_dict': make_sim_dict(Gui),
        'queen_dict': make_queen_dict(Gui),
        'domain_dict': make_domain_dict(Gui),
        'deposit_dict': make_deposit_dict(Gui),
        'gauss_dict': make_gauss_dict(Gui),
    }

def get_best():
    " return the id of the best sim "
    from cythonic.plugins.db_controller import db_controller
    from cythonic.plugins.db_path import db_path
    db = db_controller(db_path(), 'stigmergy.db')
    qry = "select sim.id from sim left join results as r on r.sim_id = sim.id where r.nestcount = (select max(r.nestcount) from sim left join results as r on r.sim_id = sim.id where sim.steps_recorded is not null and sim.steps_recorded > 100) limit 1"
    row, _ = db.return_all(qry) # result should be a 2 dimensional row of length 1
    db.close()
    return row[0][0]
