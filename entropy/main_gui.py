import sys
from PyQt5 import QtWidgets, uic
from gui_files.simmer import Ui_MainWindow

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_( ))
