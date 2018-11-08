# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'entropy/gui_files/simmer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 771, 511))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_results = QtWidgets.QWidget()
        self.tab_results.setObjectName("tab_results")
        self.tabWidget.addTab(self.tab_results, "")
        self.tab_sim = QtWidgets.QWidget()
        self.tab_sim.setObjectName("tab_sim")
        self.tabWidget.addTab(self.tab_sim, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_results), _translate("MainWindow", "Results"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_sim), _translate("MainWindow", "New Simulation"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.actionQuit.setText(_translate("MainWindow", "Quit()"))

