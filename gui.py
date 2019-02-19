from gui.sim_launcher import Ui_MainWindow
import sys
import animate_sim
from PyQt5 import QtWidgets, uic,QtCore

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
        self.menu()
        self.connect_buttons()
        # self.list_sims_tab()

    def connect_buttons(self,):
        self.ui.replay_btn.clicked.connect(self.replay_sim)

    def set_text(self, txt):
        _translate = QtCore.QCoreApplication.translate
        disp_text = add_textbox(txt)
        self.ui.textbox_status.setHtml(_translate("MainWindow", disp_text))

    def menu(self):
        " attach the menu items to actions "
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)

    def replay_sim(self,):
        " launch a new simulation "
        sim_id = int(self.ui.sim_id_input.text())
        self.set_text(f'Showing sim {sim_id}')
        animate_sim.show_plot(sim_id, colormap = 'plasma')

    # def list_sims_tab(self):
    #     " fill the sim player tab with items "
    #     # self.ui.scrollArea.setWidget(self.ui.verticalLayout)
    #     experiment = []
    #     for i in range(15):
    #         box = QtWidgets.QTextBrowser(self.ui.scrollAreaWidgetContents)
    #         experiment.append(box)
    #         box.setMaximumSize(QtCore.QSize(500, 100))
    #         box.setMinimumSize(QtCore.QSize(500, 100))
    #         box.setObjectName("simPropertiesDisplay"+str(i))
    #         self.ui.verticalLayout.addWidget(box)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_( ))
