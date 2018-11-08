import sys
from PyQt5 import QtWidgets, uic,QtCore
from gui_files.simmer import Ui_MainWindow

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menu()
        self.list_sims_tab()

    def menu(self):
        " attach the menu items to actions "
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)

    def list_sims_tab(self):
        " fill the sim player tab with items "
        self.simPropertiesDisplay2 = QtWidgets.QTextBrowser(self.ui.verticalLayoutWidget)
        self.simPropertiesDisplay2.setMaximumSize(QtCore.QSize(500, 100))
        self.simPropertiesDisplay2.setObjectName("simPropertiesDisplay2")
        self.ui.verticalLayout.addWidget(self.simPropertiesDisplay2)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_( ))
