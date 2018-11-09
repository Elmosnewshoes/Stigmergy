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
        # self.ui.scrollArea.setWidget(self.ui.verticalLayout)
        experiment = []
        for i in range(15):
            box = QtWidgets.QTextBrowser(self.ui.scrollAreaWidgetContents)
            experiment.append(box)
            box.setMaximumSize(QtCore.QSize(500, 100))
            box.setMinimumSize(QtCore.QSize(500, 100))
            box.setObjectName("simPropertiesDisplay"+str(i))
            self.ui.verticalLayout.addWidget(box)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_( ))
