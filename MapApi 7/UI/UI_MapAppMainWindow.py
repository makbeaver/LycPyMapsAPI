# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MapAppMainWindow(object):
    def setupUi(self, MapAppMainWindow):
        MapAppMainWindow.setObjectName("MapAppMainWindow")
        MapAppMainWindow.resize(682, 457)
        self.centralwidget = QtWidgets.QWidget(MapAppMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.map_label = ScalingImage(self.centralwidget)
        self.map_label.setObjectName("map_label")
        self.gridLayout.addWidget(self.map_label, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.map_type_box = QtWidgets.QComboBox(self.centralwidget)
        self.map_type_box.setFocusPolicy(QtCore.Qt.NoFocus)
        self.map_type_box.setObjectName("map_type_box")
        self.map_type_box.addItem("")
        self.map_type_box.addItem("")
        self.horizontalLayout.addWidget(self.map_type_box)
        self.go_names_btn = QtWidgets.QPushButton(self.centralwidget)
        self.go_names_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.go_names_btn.setCheckable(True)
        self.go_names_btn.setObjectName("go_names_btn")
        self.horizontalLayout.addWidget(self.go_names_btn)
        self.traffic_jams_btn = QtWidgets.QPushButton(self.centralwidget)
        self.traffic_jams_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.traffic_jams_btn.setCheckable(True)
        self.traffic_jams_btn.setObjectName("traffic_jams_btn")
        self.horizontalLayout.addWidget(self.traffic_jams_btn)
        self.object_input = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.object_input.sizePolicy().hasHeightForWidth())
        self.object_input.setSizePolicy(sizePolicy)
        self.object_input.setMinimumSize(QtCore.QSize(0, 0))
        self.object_input.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.object_input.setText("")
        self.object_input.setObjectName("object_input")
        self.horizontalLayout.addWidget(self.object_input)
        self.find_obj_btn = QtWidgets.QPushButton(self.centralwidget)
        self.find_obj_btn.setObjectName("find_obj_btn")
        self.horizontalLayout.addWidget(self.find_obj_btn)
        self.reset_result_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reset_result_btn.setObjectName("reset_result_btn")
        self.horizontalLayout.addWidget(self.reset_result_btn)
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setText("")
        self.info_label.setObjectName("info_label")
        self.horizontalLayout.addWidget(self.info_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.setRowStretch(1, 1)
        MapAppMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MapAppMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 682, 21))
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
        self.map_type_box.setItemText(0, _translate("MapAppMainWindow", "схема"))
        self.map_type_box.setItemText(1, _translate("MapAppMainWindow", "спутник"))
        self.go_names_btn.setText(_translate("MapAppMainWindow", "названия"))
        self.traffic_jams_btn.setText(_translate("MapAppMainWindow", "пробки"))
        self.object_input.setPlaceholderText(_translate("MapAppMainWindow", "введите запрос для поиска объекта"))
        self.find_obj_btn.setText(_translate("MapAppMainWindow", "искать"))
        self.reset_result_btn.setText(_translate("MapAppMainWindow", "сброс поискового результата"))
from Modules.ScalingImage import ScalingImage
