import sys
import pyvisa
import visa

from PyQt4 import QtGui, QtCore
from cmw500auto import Ui_CMW500AutomationTool
from cellPowerManager import CellPowerTest


class AttenuationManager(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.uiAM = Ui_CMW500AutomationTool()
        self.uiAM.setupUi(self)

        self.uiAM.labelDisconect.setText("<font color='red'>Disconnect</font>")
        # self.uiAM.pushButtonStart.setEnabled(True)

        # Signals and slots
        self.uiAM.pushButtonConnect.clicked.connect(self.test_connection_to_cmw)
        self.uiAM.pushButtonStart.clicked.connect(self.attenuation_test)


    def test_connection_to_cmw(self):
        okno, self.connect_address, ok = Connection_Test.cmw_connect()
        okno = okno.split(',')
        if ok:
            if okno[0] == 'Rohde&Schwarz' and okno[1] == 'CMW':
                self.uiAM.labelDisconect.setText("<font color='green'>Connected</font>")
                self.uiAM.pushButtonStart.setEnabled(True)
                QtGui.QMessageBox.information(self, 'Information',
                                              'Connection to CMW-500 has been established correctly.\n\n'
                                              + okno[0] + ', ' + okno[1] + ',\n'
                                              + 'Serial no.: ' + okno[2] + ',\n'
                                              + 'Soft: ' + okno[3])

    def attenuation_test(self):
        self.connect_address='TCPIP0::192.168.100.1::hislip0::INSTR'
        if self.uiAM.checkBoxRF1.isChecked() and self.uiAM.checkBoxRF2.isChecked():
            self.cell_power = CellPowerTest(connect_address=self.connect_address,
                                            cell_test_loop=self.uiAM.lineEditLoop.text(),

                                            cell_1_power_min=self.uiAM.lineEditRF1min.text(),
                                            cell_1_power_max=self.uiAM.lineEditRF1max.text(),
                                            cell_1_step=self.uiAM.lineEditRF1Step.text(),
                                            cell_1_time=self.uiAM.lineEditRF1Time.text(),

                                            cell_2_power_min=self.uiAM.lineEditRF2min.text(),
                                            cell_2_power_max=self.uiAM.lineEditRF2max.text(),
                                            cell_2_step=self.uiAM.lineEditRF2Step.text(),
                                            cell_2_time=self.uiAM.lineEditRF2Time.text(),
                                            channel_to_test='0')
            self.cell_power.start()

        elif self.uiAM.checkBoxRF1.isChecked():
            self.cell_power = CellPowerTest(connect_address=self.connect_address,
                                            cell_1_power_min=self.uiAM.lineEditRF1min.text(),
                                            cell_1_power_max=self.uiAM.lineEditRF1max.text(),
                                            cell_1_step=self.uiAM.lineEditRF1Step.text(),
                                            cell_1_time=self.uiAM.lineEditRF1Time.text(),
                                            cell_test_loop=self.uiAM.lineEditLoop.text(),
                                            channel_to_test='1')
            self.cell_power.start()
        elif self.uiAM.checkBoxRF2.isChecked():
            self.cell_power = CellPowerTest(connect_address=self.connect_address,
                                            cell_2_power_min=self.uiAM.lineEditRF2min.text(),
                                            cell_2_power_max=self.uiAM.lineEditRF2max.text(),
                                            cell_2_step=self.uiAM.lineEditRF2Step.text(),
                                            cell_2_time=self.uiAM.lineEditRF2Time.text(),
                                            cell_test_loop=self.uiAM.lineEditLoop.text(),
                                            channel_to_test='2')

            self.cell_power.start()

        else:
            QtGui.QMessageBox.warning(self, 'Warning', 'Select any checkBox under channels if you want to start test')


class Connection_Test(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Connection_Test, self).__init__(parent)
        # Rohde Schwarz zasoby
        self.rm = visa.ResourceManager()

        # Window structure
        resourceLabel = QtGui.QLabel('Resource')
        self.resourceWindow = QtGui.QTextEdit()
        self.connectWindow = QtGui.QLineEdit()
        self.connectWindow.setText('TCPIP0::192.168.100.1::hislip0::INSTR')
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
                                              QtCore.Qt.Horizontal, self)
        ukladV = QtGui.QHBoxLayout()
        # ukladV.addWidget(self.connectButton)
        ukladV.addWidget(self.buttons)


        uklad = QtGui.QGridLayout(self)
        uklad.addWidget(resourceLabel, 0, 0)
        uklad.addWidget(self.resourceWindow, 1, 0)
        uklad.addWidget(self.connectWindow, 2, 0)
        uklad.addLayout(ukladV, 3, 0, 3, 0)

        # self.connectButton.clicked.connect(self.start_test_connection)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setWindowTitle('Connection Manager')
        self.setModal(True)


    def find_resources(self):
        resource = self.rm.list_resources()
        # self.resourceWindow.clear()
        for item in list(resource):
            self.resourceWindow.append(item)

    def start_test_connection(self):
        try:
            instr = self.rm.open_resource(self.connectWindow.text())
            return (instr.query("*IDN?"), self.connectWindow.text())
        except pyvisa.errors.VisaIOError as e:
            QtGui.QMessageBox.warning(self, 'Error!!!', 'Error during connection to CMW-500:\n' + str(e),
                                      QtGui.QMessageBox.Ok)
            return ('Error during connection to CMW-500:\n' + str(e))

    @staticmethod
    def cmw_connect(parent=None):
        okno = Connection_Test(parent)
        okno.show()
        okno.find_resources()
        ok = okno.exec_()
        result, connect_addres = okno.start_test_connection()
        return (result, connect_addres, ok == QtGui.QDialog.Accepted)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = AttenuationManager()
    myapp.show()
    sys.exit(app.exec())
