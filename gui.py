# =======================================
# Created by: Bram Durieux
#   as part of the master thesis at the Delft University of Technology
#
# Description: Main file, launches the Graphical User Interface for theANT3000 simulator
# =======================================
from gui.sim_launcher import Ui_MainWindow
import sys
import animate_sim
from PyQt5 import QtWidgets, uic,QtCore
import json
import os
from cythonic.plugins.gui_functions import *
from cythonic.core.sim_player import extract_settings
from cythonic.plugins.queries import get_settings
from cythonic.plugins.db_path import db_path
from cythonic.plugins.db_controller import db_controller
import math

from record_and_play import record_and_play
_translate = QtCore.QCoreApplication.translate
settings_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])+'/gui/gui_data.json'


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.i = iterator() # keep track of messages (self.textlines)
        self.textlines = [] # holds messages to display at the gui
        self.connect_buttons()
        self.welcome_message()
        self.db = db_controller(db_path(),'stigmergy.db')
        self.load_best()
        data = self.get_settings()
        if data:
            self.load_settings(**data)
    def load_best(self):
        " display the best simulation in the sim_id field "
        self.ui.sim_id_input.setText(_translate("MainWindow", str(get_best(self.db))))

    def welcome_message(self):
        self.set_text('--Welcome to theANT<span style=" vertical-align:super;">3000</span> &#8482; --')

    def run_sim(self,):
        record = self.ui.check_recording.isChecked()
        visualize = self.ui.check_visualize.isChecked()
        dicts = simulation_args(self.ui)
        input_status, msg = validate_settings(dicts)
        store_interval = self.ui.spinbox_interval.value()
        if input_status < 0:
            " checks do not compute, terminate function call "
            self.set_text(msg)
            return
        elif input_status < 1:
            " just warn "
            self.set_text(msg)

        if visualize and not record:
            " live simulation but do not write the results to the database "
            self.set_text('Not implemented yet')
            return
        else:
            self.set_text('Preparing a new simulation')
            result = record_and_play(**dicts, record= record, upload_interval = store_interval, visualize = visualize)
        t = f" Simulation # {result['sim_id']}" +\
            f" yielded a nestcount score of {result['nestcount']} with {dicts['sim_dict']['n_agents']} ants" +\
            f" -> efficiency of &eta; = {round(result['score']*1e6,2)} 10<sup>-6</sup>ants/sec"
        self.set_text(t)

    def save_and_quit(self):
        " exit app gracefully but save the settigns first "
        self.store_settings()
        QtCore.QCoreApplication.instance().quit()

    def connect_buttons(self,):
        self.ui.actionQuit.triggered.connect(self.save_and_quit)
        self.ui.replay_btn.clicked.connect(self.replay_sim)
        self.ui.copy_btn.clicked.connect(self.copy_settings)
        self.ui.button_run.clicked.connect(self.run_sim)

    def set_text(self, txt):
        disp_text = add_textbox(self,txt)
        self.ui.textbox_status.setHtml(_translate("MainWindow", disp_text))

    def replay_sim(self,):
        " launch a new simulation "
        sim_id = int(self.ui.sim_id_input.text())
        status = animate_sim.show_plot(sim_id, colormap = 'plasma')
        if status < 0:
            self.set_text(f'No rows for simulation {sim_id}')
        elif status ==0:
            # show only the results
            self.set_text(f'Showing the results of {sim_id}')
        else:
            # simulation is recorded, showing
            self.set_text(f'Showing sim {sim_id}')

    def load_settings(self, sim_dict, queen_dict,
                      domain_dict, gauss_dict, deposit_dict):
        " wrapper for the load_setings function in gui_functions.py"
        load_settings(self.ui, sim_dict, queen_dict, domain_dict, gauss_dict, deposit_dict)

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

    def copy_settings(self):
        " get settings from a specific simulation from the database "
        sim_id = int(self.ui.sim_id_input.text())
        sim_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'sim_settings')))
        domain_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'domain_settings')))
        queen_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'queen_settings')))
        ant_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'ant_settings')))
        sens_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'sens_settings')))
        gauss_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'gauss_settings')))
        deposit_dict = extract_settings(*self.db.return_all(get_settings(sim_id,'deposit_settings')))
        ant_dict['sens_dict'] = sens_dict
        queen_dict['ant_dict'] = ant_dict
        sim_dict['deploy_timing_args'] = eval(sim_dict['deploy_timing_args'])
        domain_dict['size'] = eval(domain_dict['size'])
        domain_dict['food_loc'] = eval(domain_dict['food_loc'])
        domain_dict['nest_loc'] = eval(domain_dict['nest_loc'])
        gauss_dict['significancy'] = math.log10(gauss_dict['significancy'])
        self.load_settings(sim_dict, queen_dict, domain_dict, gauss_dict, deposit_dict)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_( ))
