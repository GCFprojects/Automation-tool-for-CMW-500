# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cmw500ManagerWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CMW500_Manager(object):
    def setupUi(self, CMW500_Manager):
        CMW500_Manager.setObjectName(_fromUtf8("CMW500_Manager"))
        CMW500_Manager.resize(601, 270)
        self.centralwidget = QtGui.QWidget(CMW500_Manager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButtonStart = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStart.setGeometry(QtCore.QRect(350, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButtonStart.setFont(font)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.pushButtonConnect = QtGui.QPushButton(self.centralwidget)
        self.pushButtonConnect.setGeometry(QtCore.QRect(20, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButtonConnect.setFont(font)
        self.pushButtonConnect.setObjectName(_fromUtf8("pushButtonConnect"))
        self.pushButtonClose = QtGui.QPushButton(self.centralwidget)
        self.pushButtonClose.setGeometry(QtCore.QRect(480, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.labelDisconect = QtGui.QLabel(self.centralwidget)
        self.labelDisconect.setEnabled(False)
        self.labelDisconect.setGeometry(QtCore.QRect(140, 185, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelDisconect.setFont(font)
        self.labelDisconect.setFrameShape(QtGui.QFrame.Panel)
        self.labelDisconect.setTextFormat(QtCore.Qt.AutoText)
        self.labelDisconect.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDisconect.setTextInteractionFlags(QtCore.Qt.TextEditable)
        self.labelDisconect.setObjectName(_fromUtf8("labelDisconect"))
        self.groupBoxCellPower = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxCellPower.setGeometry(QtCore.QRect(10, 20, 191, 51))
        self.groupBoxCellPower.setTitle(_fromUtf8(""))
        self.groupBoxCellPower.setObjectName(_fromUtf8("groupBoxCellPower"))
        self.checkBoxCellPower = QtGui.QCheckBox(self.groupBoxCellPower)
        self.checkBoxCellPower.setGeometry(QtCore.QRect(10, 10, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBoxCellPower.setFont(font)
        self.checkBoxCellPower.setObjectName(_fromUtf8("checkBoxCellPower"))
        self.pushButtonShowCellPower = QtGui.QPushButton(self.centralwidget)
        self.pushButtonShowCellPower.setGeometry(QtCore.QRect(210, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButtonShowCellPower.setFont(font)
        self.pushButtonShowCellPower.setObjectName(_fromUtf8("pushButtonShowCellPower"))
        CMW500_Manager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(CMW500_Manager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 601, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        CMW500_Manager.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(CMW500_Manager)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        CMW500_Manager.setStatusBar(self.statusbar)

        self.retranslateUi(CMW500_Manager)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), CMW500_Manager.close)
        QtCore.QMetaObject.connectSlotsByName(CMW500_Manager)

    def retranslateUi(self, CMW500_Manager):
        CMW500_Manager.setWindowTitle(_translate("CMW500_Manager", "CMW-500 Manager", None))
        self.pushButtonStart.setText(_translate("CMW500_Manager", "Start", None))
        self.pushButtonConnect.setText(_translate("CMW500_Manager", "Connect", None))
        self.pushButtonClose.setText(_translate("CMW500_Manager", "Close", None))
        self.labelDisconect.setText(_translate("CMW500_Manager", "Not connected", None))
        self.checkBoxCellPower.setText(_translate("CMW500_Manager", "Cell Power Manager", None))
        self.pushButtonShowCellPower.setText(_translate("CMW500_Manager", "Show", None))

