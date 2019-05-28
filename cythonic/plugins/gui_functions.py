# store some functions (methods) here to declutter the gui.py file in the main directory
from PyQt5 import QtCore
_translate = QtCore.QCoreApplication.translate
def make_domain_dict(Gui):
    the_dict = {
        'size': [Gui.dom_x_size.value(),Gui.dom_y_size.value()],
        'pitch': Gui.spinbox_pitch.value(),
        'nest_loc': [Gui.nest_x_size.value(), Gui.nest_y_size.value()],
        'nest_rad': Gui.spinbox_nestradius.value(),
        'food_loc': [Gui.food_x_size.value(), Gui.food_y_size.value()],
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
        'noise_gain2': Gui.spinbox_noisegain_2.value(),
        'steer_regularization': Gui.spinbox_regularization.value(),
        'rotate_fun': Gui.combobox_rotate.currentText(),
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

def validate_settings(dicts):
    " do sanity checks, raise error "
    status = 1
    msg = ""
    " check if food is in domain "
    if (dicts['domain_dict']['food_loc'][0] > dicts['domain_dict']['size'][0]-dicts['domain_dict']['food_rad']
        or dicts['domain_dict']['food_loc'][1] > dicts['domain_dict']['size'][1]-dicts['domain_dict']['food_rad']):
        status = -1
        msg = "Food location out of bounds"
        return status, msg
    if (dicts['domain_dict']['nest_loc'][0] > dicts['domain_dict']['size'][0]-dicts['domain_dict']['nest_rad']
        or dicts['domain_dict']['nest_loc'][1] > dicts['domain_dict']['size'][1]-dicts['domain_dict']['nest_rad']):
        status = -1
        msg = "Food location out of bounds"
        return status, msg

    return status, msg

def get_best(db, ):
    " return the id of the best sim "
    qry = "select sim.id from sim left join results as r on r.sim_id = sim.id where r.nestcount = (select max(r.nestcount) from sim left join results as r on r.sim_id = sim.id where sim.steps_recorded is not null and sim.steps_recorded > 100) limit 1"
    try:
        "first, check if db is populated, then find the best simulation "
        row, _ = db.return_all(qry) # result should be a 2 dimensional row of length 1
        return get_best_score(db)['ID'].astype(int)
    except:
        row = [[0]]
        return row[0][0]

def load_settings(Gui, sim_dict, queen_dict,
                  domain_dict, gauss_dict, deposit_dict):
    " restore all fields from text file "
    " domain "

    # Gui.dom_x_size.setProperty('value', 3333)
    Gui.dom_x_size.setProperty('value', domain_dict['size'][0])
    Gui.dom_y_size.setProperty('value', domain_dict['size'][1])
    Gui.spinbox_pitch.setProperty('value', domain_dict['pitch'])
    Gui.nest_x_size.setProperty('value', domain_dict['nest_loc'][0])
    Gui.nest_y_size.setProperty('value', domain_dict['nest_loc'][1])
    Gui.spinbox_nestradius.setProperty('value', domain_dict['nest_rad'])
    Gui.food_x_size.setProperty('value', domain_dict['food_loc'][0])
    Gui.food_y_size.setProperty('value', domain_dict['food_loc'][1])
    Gui.spinbox_foodradius.setProperty('value', domain_dict['food_rad'])
    Gui.spinbox_pheromone.setProperty('value', domain_dict['target_pheromone'])
    #
    " sim "
    # Gui.sim_id_input.setText(_translate("MainWindow", best_sim))
    Gui.spinbox_agents.setProperty('value', sim_dict['n_agents'])
    Gui.spinbox_dt.setProperty('value', sim_dict['dt'])
    Gui.spinbox_steps.setProperty('value', sim_dict['steps'])
    Gui.combobox_deployment.setCurrentText(_translate("MainWindow", sim_dict['deploy_style']))
    Gui.combobox_timing.setCurrentText(_translate("MainWindow", sim_dict['deploy_timing']))
    Gui.spinbox_deployk.setProperty('value', sim_dict['deploy_timing_args']['k'])
    Gui.spinbox_deploytheta.setProperty('value', sim_dict['deploy_timing_args']['teta'])
    try: # not always contained in the sim dictionary
        Gui.spinbox_deploytmax.setProperty('value', sim_dict['deploy_timing_args']['t_max'])
    except:
        pass
    Gui.spinbox_evaporation.setProperty('value', sim_dict['evap_rate'])
    #
    " queen "
    Gui.spinbox_speed.setProperty('value', queen_dict['default_speed'])
    Gui.combobox_noise.setCurrentText(_translate("MainWindow", queen_dict['noise_type']))
    Gui.line_noiseparameter.setText(_translate("MainWindow", str(queen_dict['noise_parameter'])))
    #
    " ant "
    Gui.spinbox_antsize.setProperty('value', queen_dict['ant_dict']['l'])
    Gui.spinbox_offset.setProperty('value', queen_dict['ant_dict']['sens_offset'])
    Gui.spinbox_gain.setProperty('value', queen_dict['ant_dict']['gain'])
    try:
        Gui.spinbox_noisegain.setProperty('value', queen_dict['ant_dict']['noise_gain'])
    except:
        Gui.spinbox_noisegain.setProperty('value', queen_dict['ant_dict']['noise_gain_1'])
    if 'steer_regularization' in queen_dict['ant_dict']:
        Gui.spinbox_regularization.setProperty('value', queen_dict['ant_dict']['steer_regularization'])
    else:
        Gui.spinbox_regularization.setProperty('value', 0.0)
    if 'noise_gain2'  in queen_dict['ant_dict']:
        Gui.spinbox_noisegain_2.setProperty('value', queen_dict['ant_dict']['noise_gain2'])
        Gui.combobox_rotate.setCurrentText(_translate("MainWindow", queen_dict['ant_dict']['rotate_fun']))
    else:
        Gui.spinbox_noisegain_2.setProperty('value', 0.0)
        Gui.combobox_rotate.setCurrentText(_translate("MainWindow", 'simple'))
    Gui.combobox_activation.setCurrentText(_translate("MainWindow", queen_dict['ant_dict']['sens_fun']))
    Gui.spinbox_breakpoint.setProperty('value', queen_dict['ant_dict']['sens_dict']['breakpoint'])
    Gui.spinbox_lambda.setProperty('value', queen_dict['ant_dict']['sens_dict']['exp_lambda'])
    val = queen_dict['ant_dict']['deposit_fun']
    if val =='exp_decay':
        Gui.combobox_depfun.setCurrentText(_translate("MainWindow", 'exponential'))
    else:
        Gui.combobox_depfun.setCurrentText(_translate("MainWindow", val))
    #
    " Gaussian "
    Gui.spinbox_significancy.setProperty('value', gauss_dict['significancy'])
    Gui.spinbox_covariance.setProperty('value', gauss_dict['covariance'])
    #
    " deposit "
    Gui.spinbox_q.setProperty('value', deposit_dict['q'])
    Gui.spinbox_returnfactor.setProperty('value', deposit_dict['return_factor'])
    Gui.spinbox_depositbeta.setProperty('value', deposit_dict['beta'])

def add_textbox(window, txt):
    lines = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"+\
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"+\
            "p, li {{ white-space: pre-wrap; }}\n"+\
            "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"+\
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">{placeholder}</p></body></html>"
    window.textlines.append(f"<p>{window.i.next}: {txt} </p> ")
    mx = len(window.textlines)
    mn = max(mx-10, 0)
    newlines = " ".join([l for l in window.textlines[mn:mx]])
    return lines.format(placeholder = newlines)

class iterator():
    def reset(self ):
        self.__init__()

    def __init__(self):
        self.i = 0
    def __add__(self, other):
        self.i+=other
        return self.value

    @property
    def next(self):
        return self.__add__(1)

    @property
    def value(self):
        return self.i
    @value.setter
    def value(self,x):
        self.i = x
    def __radd__(self,other):
        if other ==0:
            return self.i
        else:
            return self.__add__(other)
def printall(Gui):
    print(f"Recording: {Gui.check_recording.isChecked()}")
    print(f"Visualize after recording: {Gui.check_visualize.isChecked()}")
    print(make_ant_dict(Gui))
    print(make_queen_dict(Gui))
    print(make_sim_dict(Gui))
    print(make_gauss_dict(Gui))
    print(make_deposit_dict(Gui))
    print(make_domain_dict(Gui))

def get_best_score(db, sim_id = -1):
    # from cythonic.plugins.db_controller import db_controller
    # from cythonic.plugins.db_path import db_path
    import numpy as np

    # db = db_controller(db_path(),'stigmergy.db')

    qry = """
        select
        sim.id,
        cast(substr(nest_loc,2,instr(nest_loc,', ')-2) as numeric) as X1,
        cast(substr(nest_loc,instr(nest_loc,', ')+2,instr(nest_loc,']')-instr(nest_loc,', ')-2) as numeric) as Y1,
        cast(substr(food_loc,2,instr(nest_loc,', ')-2) as numeric) as X2,
        cast(substr(food_loc,instr(nest_loc,', ')+2,instr(nest_loc,']')-instr(nest_loc,', ')-2) as numeric) as Y2,
        dom.food_rad, dom.nest_rad,
        cast(sim_s.steps as numeric) * sim_s.dt as T,
        queen.default_speed as S,
        results.nestcount as nestcount,
        sim.steps_recorded
        from sim
        left join domain_settings dom on dom.sim_id = sim.id
        left join sim_settings as sim_s on sim_s.sim_id = sim.id
        left join queen_settings as queen on queen.sim_id = sim.id
        left join results on results.sim_id = sim.id
        where dom.sim_id is not null
        AND sim.status = 'FINISHED'
        AND sim_s.sim_id is not null
        AND queen.sim_id is not null
        AND queen.default_speed is not null
        AND sim_s.dt is not null
        AND sim_s.steps is not null
        AND results.sim_id is not null
        AND results.nestcount is not null
        """
    if sim_id >= 0:
        " if specific sim is requested "
        qry+= f" AND sim.id = {sim_id}"

    df = db.get_df(qry)
    df['R'] = np.sqrt(np.power(df['X1']-df['X2'],2)+np.power(df['Y1']-df['Y2'],2))-df['food_rad']-df['nest_rad']
    df['score'] = 1e6*df['nestcount'] * df['R'] / (df['steps_recorded'] * df['S'] * df['T'])
    # print(df[['ID','R','S','T','steps_recorded','score']].sort_values(by='score',ascending= False))
    # print(df[['ID','R','S','T','steps_recorded','score']].sort_values(by='score',ascending= False).iloc[0]['ID'])
    return df[['ID','R','S','T','steps_recorded','score']].sort_values(by='score',ascending= False).iloc[0]
