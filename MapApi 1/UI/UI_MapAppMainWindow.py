# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MapAppMainWindow(object):
    def setupUi(self, MapAppMainWindow):
        MapAppMainWindow.setObjectName("MapAppMainWindow")
        MapAppMainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MapAppMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.map_label = QtWidgets.QLabel(self.centralwidget)
        self.map_label.setText("")
        self.map_label.setObjectName("map_label")
        self.gridLayout.addWidget(self.map_label, 0, 0, 1, 1)
        MapAppMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MapAppMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MapAppMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MapAppMainWindow)
        self.statusbar.setObjectName("statusbar")
        MapAppMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MapAppMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MapAppMainWindow)

    def retranslateUi(self, MapAppMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MapAppMainWindow.setWindowTitle(_translate("MapAppMainWindow", "Поисковое приложение"))
