from gui.sim_launcher import Ui_MainWindow
import sys
import animate_sim
from PyQt5 import QtWidgets, uic,QtCore
import json
import os
from cythonic.plugins.gui_functions import make_ant_dict, make_deposit_dict, make_domain_dict, make_gauss_dict
from cythonic.plugins.gui_functions import make_queen_dict, make_sim_dict, simulation_args, get_best

from record_and_play import record_and_play
_translate = QtCore.QCoreApplication.translate
settings_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])+'/gui/gui_data.json'
textlines = []
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

i = iterator()

def add_textbox(txt):
    lines = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"+\
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"+\
            "p, li {{ white-space: pre-wrap; }}\n"+\
            "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"+\
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">{placeholder}</p></body></html>"
    textlines.append(f"<p>{i.next}: {txt} </p> ")
    mx = len(textlines)
    mn = max(mx-10, 0)
    newlines = " ".join([l for l in textlines[mn:mx]])
    return lines.format(placeholder = newlines)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_buttons()
        self.welcome_message()
        data = self.get_settings()
        if data:
            self.load_settings(**data)

    def welcome_message(self):
        self.set_text('-- Welcome to ANT<span style=" vertical-align:super;">3000</span> &#8482; </p>')

    def run_sim(self,):
        record = self.ui.check_recording.isChecked()
        visualize = self.ui.check_visualize.isChecked()

        if record:
            " first record the sim, then play the replay "
            store_interval = self.ui.spinbox_interval.value()
            record_and_play(**simulation_args(self.ui), record= record, upload_interval = store_interval)
        elif visualize:
            " live simulation but do not write the results to the database "
        else:
            " only print the result, no visualization, do not store to database "

    def connect_buttons(self,):
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.replay_btn.clicked.connect(self.replay_sim)
        self.ui.copy_btn.clicked.connect(self.store_settings)
        self.ui.button_run.clicked.connect(self.run_sim)

    def set_text(self, txt):
        disp_text = add_textbox(txt)
        self.ui.textbox_status.setHtml(_translate("MainWindow", disp_text))

    def replay_sim(self,):
        " launch a new simulation "
        sim_id = int(self.ui.sim_id_input.text())
        status = animate_sim.show_plot(sim_id, colormap = 'plasma')
        if status <= 0:
            self.set_text(f'No rows for simulation {sim_id}')
        else:
            self.set_text(f'Showing sim {sim_id}')

    def printall(self):
        print(f"Recording: {self.ui.check_recording.isChecked()}")
        print(f"Visualize after recording: {self.ui.check_visualize.isChecked()}")
        print(make_ant_dict(self.ui))
        print(make_queen_dict(self.ui))
        print(make_sim_dict(self.ui))
        print(make_gauss_dict(self.ui))
        print(make_deposit_dict(self.ui))
        print(make_domain_dict(self.ui))

    def load_settings(self, sim_dict, queen_dict,
                      domain_dict, gauss_dict, deposit_dict):
        " restore all fields from text file "
        " domain "
        self.ui.dom_x_size.setProperty('value', domain_dict['size'][1])
        self.ui.dom_x_size.setProperty('value', domain_dict['size'][0])
        self.ui.spinbox_pitch.setProperty('value', domain_dict['pitch'])
        self.ui.nest_x_size.setProperty('value', domain_dict['nest_loc'][0])
        self.ui.nest_x_size.setProperty('value', domain_dict['nest_loc'][1])
        self.ui.spinbox_nestradius.setProperty('value', domain_dict['nest_rad'])
        self.ui.food_x_size.setProperty('value', domain_dict['food_loc'][0])
        self.ui.food_x_size.setProperty('value', domain_dict['food_loc'][1])
        self.ui.spinbox_foodradius.setProperty('value', domain_dict['food_rad'])
        self.ui.spinbox_pheromone.setProperty('value', domain_dict['target_pheromone'])
        #
        " sim "
        best_sim = str(get_best())
        print(best_sim)
        self.ui.sim_id_input.setText(_translate("MainWindow", best_sim))
        self.ui.spinbox_agents.setProperty('value', sim_dict['n_agents'])
        self.ui.spinbox_dt.setProperty('value', sim_dict['dt'])
        self.ui.spinbox_steps.setProperty('value', sim_dict['steps'])
        self.ui.combobox_deployment.setCurrentText(_translate("MainWindow", sim_dict['deploy_style']))
        self.ui.combobox_timing.setCurrentText(_translate("MainWindow", sim_dict['deploy_timing']))
        self.ui.spinbox_deployk.setProperty('value', sim_dict['deploy_timing_args']['k'])
        self.ui.spinbox_deploytheta.setProperty('value', sim_dict['deploy_timing_args']['teta'])
        self.ui.spinbox_deploytmax.setProperty('value', sim_dict['deploy_timing_args']['t_max'])
        self.ui.spinbox_evaporation.setProperty('value', sim_dict['evap_rate'])
        #
        " queen "
        self.ui.spinbox_speed.setProperty('value', queen_dict['default_speed'])
        self.ui.combobox_noise.setCurrentText(_translate("MainWindow", queen_dict['noise_type']))
        self.ui.line_noiseparameter.setText(_translate("MainWindow", str(queen_dict['noise_parameter'])))
        #
        " ant "
        self.ui.spinbox_antsize.setProperty('value', queen_dict['ant_dict']['l'])
        self.ui.spinbox_offset.setProperty('value', queen_dict['ant_dict']['sens_offset'])
        self.ui.spinbox_gain.setProperty('value', queen_dict['ant_dict']['gain'])
        self.ui.spinbox_noisegain.setProperty('value', queen_dict['ant_dict']['noise_gain'])
        self.ui.combobox_activation.setCurrentText(_translate("MainWindow", queen_dict['ant_dict']['sens_fun']))
        self.ui.spinbox_breakpoint.setProperty('value', queen_dict['ant_dict']['sens_dict']['breakpoint'])
        self.ui.spinbox_lambda.setProperty('value', queen_dict['ant_dict']['sens_dict']['exp_lambda'])
        val = queen_dict['ant_dict']['deposit_fun']
        if val =='exp_decay':
            self.ui.combobox_depfun.setCurrentText(_translate("MainWindow", 'exponential'))
        else:
            self.ui.combobox_depfun.setCurrentText(_translate("MainWindow", val))
        #
        " Gaussian "
        self.ui.spinbox_significancy.setProperty('value', gauss_dict['significancy'])
        self.ui.spinbox_covariance.setProperty('value', gauss_dict['covariance'])
        #
        " deposit "
        self.ui.spinbox_q.setProperty('value', deposit_dict['q'])
        self.ui.spinbox_returnfactor.setProperty('value', deposit_dict['return_factor'])
        self.ui.spinbox_depositbeta.setProperty('value', deposit_dict['beta'])

    def get_settings(self):
        " load settings from file "
        try:
            with open(settings_path) as f:
                data = json.load(f)
        except: return
        return data


    def store_settings(self):
        " store the values as in the gui to a text file to reload later on "
        with open(settings_path, 'w') as f:
            json.dump(simulation_args(self.ui), f, ensure_ascii=False)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_( ))
