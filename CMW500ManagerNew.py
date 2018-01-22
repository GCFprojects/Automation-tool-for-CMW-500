import sys
import pyvisa
import visa

from PyQt4 import QtGui, QtCore
from cellPowerManagerWindowNew import Ui_cellPowerManagerWindow
from cmw500ManagerWindowNew import Ui_CMW500_Manager
from cellPowerManagerNew import CellPowerTest


class CMW500ManagerWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.uiCMW = Ui_CMW500_Manager()
        self.uiCMW.setupUi(self)

        self.uiCMW.checkBoxCellPower.stateChanged.connect(self.cellPowerManagerWindow)
        self.uiCMW.labelDisconect.setText("<font color='red'>Not connected</font>")
        self.uiCMW.pushButtonConnect.clicked.connect(self.test_connection_to_cmw)
        self.uiCMW.pushButtonStart.setEnabled(True)
        self.uiCMW.pushButtonStart.clicked.connect(self.attenuation_test)
        self.uiCMW.pushButtonShowCellPower.hide()
        self.uiCMW.pushButtonShowCellPower.clicked.connect(self.showCellPowerManager)

    def cellPowerManagerWindow(self):
        if self.uiCMW.checkBoxCellPower.isChecked():
            self.cell_power_config = CellPowerManagerWindow.openWindow()
            if self.cell_power_config == 'None':
                self.uiCMW.checkBoxCellPower.setCheckState(False)
            else:
                self.uiCMW.pushButtonShowCellPower.show()

    def test_connection_to_cmw(self):
        okno, self.connect_address, ok = Connection_Test.cmw_connect()
        print(ok)
        okno = okno.split(',')
        if ok:
            if okno[0] == 'Rohde&Schwarz' and okno[1] == 'CMW':
                self.uiCMW.labelDisconect.setText("<font color='green'>Connected</font>")
                self.uiCMW.pushButtonStart.setEnabled(True)
                QtGui.QMessageBox.information(self, 'Information',
                                              'Connection to CMW-500 has been established correctly.\n\n'
                                              + okno[0] + ', ' + okno[1] + ',\n'
                                              + 'Serial no.: ' + okno[2] + ',\n'
                                              + 'Soft: ' + okno[3])
        # else:
        #     QtGui.QMessageBox.warning(self, 'Error!!!', ,

    def attenuation_test(self):
        self.connect_address = 'TCPIP0::192.168.100.1::hislip0::INSTR'
        if self.uiCMW.checkBoxCellPower.isChecked():
            print(self.cell_power_config)
            if self.cell_power_config[0] == 'Signaling 1 and 2 synchronously':
                self.cell_power = CellPowerTest(connect_address=self.connect_address,
                                                cell_test_loop=self.cell_power_config[9],
                                                cell_test_loop_delay=self.cell_power_config[10],

                                                cell_1_power_min=self.cell_power_config[3],
                                                cell_1_power_max=self.cell_power_config[4],
                                                cell_1_step=self.cell_power_config[7],
                                                cell_1_time=self.cell_power_config[8],

                                                cell_2_power_min=self.cell_power_config[5],
                                                cell_2_power_max=self.cell_power_config[6],
                                                cell_2_step=self.cell_power_config[7],
                                                cell_2_time=self.cell_power_config[8],
                                                channel_to_test='0')
                self.cell_power.start()

        elif self.cell_power_config[0] == 'Signaling 1':
            self.cell_power = CellPowerTest(connect_address=self.connect_address,
                                            cell_1_power_min=self.cell_power_config[2],
                                            cell_1_power_max=self.cell_power_config[3],
                                            cell_1_step=self.cell_power_config[4],
                                            cell_1_time=self.cell_power_config[5],
                                            cell_test_loop=self.cell_power_config[6],
                                            cell_test_loop_delay=self.cell_power_config[7],
                                            channel_to_test='1')
            self.cell_power.start()
        elif self.cell_power_config[0] == 'Signaling 2':
            self.cell_power = CellPowerTest(connect_address=self.connect_address,
                                            cell_2_power_min=self.cell_power_config[2],
                                            cell_2_power_max=self.cell_power_config[3],
                                            cell_2_step=self.cell_power_config[4],
                                            cell_2_time=self.cell_power_config[5],
                                            cell_test_loop=self.cell_power_config[6],
                                            cell_test_loop_delay=self.cell_power_config[7],
                                            channel_to_test='2')

            self.cell_power.start()

        else:
            QtGui.QMessageBox.warning(self, 'Warning', 'Select any checkBox under channels if you want to start test')

    def showCellPowerManager(self):

        QtGui.QMessageBox.information(self, 'Information:', 'This functionality will be enabled in the future.')


class CellPowerManagerWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CellPowerManagerWindow, self).__init__(parent)
        self.uiCPMW = Ui_cellPowerManagerWindow()
        self.uiCPMW.setupUi(self)

        self.hideGroups()
        self.uiCPMW.pushButtonSave.hide()
        self.uiCPMW.timeEditTestDuration.hide()
        self.uiCPMW.pushButtonClose.setText('Save and Close')
        self.uiCPMW.comboBoxTestType.activated.connect(self.windowView)
        self.uiCPMW.lineEditMaxSignSynch1.textChanged.connect(self.updateSign2Min)
        self.uiCPMW.lineEditMinSignSynch1.textChanged.connect(self.updateSign2Max)
        self.updateTime()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        # self.uiCPMW.timeEditTestDuration.timeout.connect(self.updateTime)


    def windowView(self):
        if self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1':
            self.hideGroups()
            self.uiCPMW.groupBoxSign1.show()
            self.uiCPMW.groupBoxLoop.show()
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 2':
            self.hideGroups()
            self.uiCPMW.groupBoxSign2.show()
            self.uiCPMW.groupBoxLoop.show()
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1 and 2 synchronously':
            self.hideGroups()
            self.uiCPMW.groupBoxSignSynch.show()
            self.uiCPMW.groupBoxLoop.show()
            self.uiCPMW.lineEditMinSignSynch2.setEnabled(False)
            self.uiCPMW.lineEditMaxSignSynch2.setEnabled(False)
        elif self.uiCPMW.comboBoxTestType.currentText() == '':
            self.hideGroups()

    def hideGroups(self):
        self.uiCPMW.groupBoxSign1.hide()
        self.uiCPMW.groupBoxSign2.hide()
        self.uiCPMW.groupBoxSignSynch.hide()
        self.uiCPMW.groupBoxLoop.hide()

    def updateTime(self):
        current = QtCore.QDateTime.currentDateTime()
        testTime = self.updateTestDuration()
        try:
            testT = QtCore.QTime(testTime[0], testTime[1],testTime[2])
            print(testT)
            a = QtCore.QDateTime(current.date(), current.time()+ testT)
            print(a)
        except TypeError:
            pass
        self.uiCPMW.dateTimeEditTestEnd.setDateTime(current)

    def updateTestDuration(self):
        if self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1':
            try:
                seconds = -(int(self.uiCPMW.lineEditMinSign1.text()) - int(self.uiCPMW.lineEditMaxSign1.text())) / \
                          int(self.uiCPMW.lineEditStepSign1.text()) * int(self.uiCPMW.lineEditTimeSign1.text()) * \
                          int(self.uiCPMW.lineEditLoop.text()) + (int(self.uiCPMW.lineEditLoop.text()) *
                                                                  int(self.uiCPMW.lineEditLoopDelay.text()))
                testTime = self.timeForTestDuration(seconds)
                text = '{0:0=2d}:{1:0=2d}:{2:0=2d}'.format(int(testTime[0]), int(testTime[1]), int(testTime[2]))
                # self.uiCPMW.timeEditTestDuration.setTe(hours, minutes, seconds)
                self.uiCPMW.lineEditTestDuration.setText(text)
                return testTime
            except (ZeroDivisionError, ValueError):
                # return 0
                pass
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 2':
            try:
                seconds = -(int(self.uiCPMW.lineEditMinSign2.text()) - int(self.uiCPMW.lineEditMaxSign2.text())) / \
                          int(self.uiCPMW.lineEditStepSign2.text()) * int(self.uiCPMW.lineEditTimeSign2.text()) * \
                          int(self.uiCPMW.lineEditLoop.text()) + (int(self.uiCPMW.lineEditLoop.text()) *
                                                                  int(self.uiCPMW.lineEditLoopDelay.text()))
                testTime = self.timeForTestDuration(seconds)
                text = '{0:0=2d}:{1:0=2d}:{2:0=2d}'.format(int(testTime[0]), int(testTime[1]), int(testTime[2]))
                # self.uiCPMW.timeEditTestDuration.setTe(hours, minutes, seconds)
                self.uiCPMW.lineEditTestDuration.setText(text)
                return testTime
            except (ZeroDivisionError, ValueError):
                # return 0
                pass
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1 and 2 synchronously':
            try:
                seconds = -(int(self.uiCPMW.lineEditMinSignSynch1.text()) - int(self.uiCPMW.lineEditMaxSignSynch1.text())) / \
                          int(self.uiCPMW.lineEditStepSignSynch.text()) * int(self.uiCPMW.lineEditTimeSignSynch.text()) * \
                          int(self.uiCPMW.lineEditLoop.text()) + (int(self.uiCPMW.lineEditLoop.text()) *
                                                                  int(self.uiCPMW.lineEditLoopDelay.text()))
                testTime = self.timeForTestDuration(seconds)
                text = '{0:0=2d}:{1:0=2d}:{2:0=2d}'.format(int(testTime[0]), int(testTime[1]), int(testTime[2]))
                # self.uiCPMW.timeEditTestDuration.setTe(hours, minutes, seconds)
                self.uiCPMW.lineEditTestDuration.setText(text)
                return testTime
            except (ZeroDivisionError, ValueError):
                # return 0
                pass

    def timeForTestDuration(self, seconds):
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60
        return [hours, minutes, seconds]

    @staticmethod
    def openWindow(parent=None):
        okno = CellPowerManagerWindow(parent)
        okno.show()
        okno.exec_()
        cell_power_config = okno.saveConfig()
        print(cell_power_config)
        # okno.close()
        return (cell_power_config)

        # self.uiCPMW = Ui_cellPowerManagerWindow()
        # self.uiCPMW.setupUi(self)

    def saveConfig(self):
        if self.uiCPMW.comboBoxTestType.currentText() == '':
            QtGui.QMessageBox.warning(self, 'Warning', 'Nie wybrałeś żadnego sygnalingu !!!')
            return 'None'
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1':
            return ([self.uiCPMW.comboBoxTestType.currentText(),
                    self.uiCPMW.comboBoxSign1.currentText(),
                    self.uiCPMW.lineEditMinSign1.text(),
                    self.uiCPMW.lineEditMaxSign1.text(),
                    self.uiCPMW.lineEditStepSign1.text(),
                    self.uiCPMW.lineEditTimeSign1.text(),
                    self.uiCPMW.lineEditLoop.text(),
                    self.uiCPMW.lineEditLoopDelay.text()])
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 2':
            return ([self.uiCPMW.comboBoxTestType.currentText(),
                     self.uiCPMW.comboBoxSign2.currentText(),
                     self.uiCPMW.lineEditMinSign2.text(),
                     self.uiCPMW.lineEditMaxSign2.text(),
                     self.uiCPMW.lineEditStepSign2.text(),
                     self.uiCPMW.lineEditTimeSign2.text(),
                     self.uiCPMW.lineEditLoop.text(),
                     self.uiCPMW.lineEditLoopDelay.text()])
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1 and 2 synchronously':
            return ([self.uiCPMW.comboBoxTestType.currentText(),
                     self.uiCPMW.comboBoxSignSynch1.currentText(),
                     self.uiCPMW.comboBoxSignSynch2.currentText(),
                     self.uiCPMW.lineEditMinSignSynch1.text(),
                     self.uiCPMW.lineEditMaxSignSynch1.text(),
                     self.uiCPMW.lineEditMinSignSynch2.text(),
                     self.uiCPMW.lineEditMaxSignSynch2.text(),
                     self.uiCPMW.lineEditStepSignSynch.text(),
                     self.uiCPMW.lineEditTimeSignSynch.text(),
                     self.uiCPMW.lineEditLoop.text(),
                     self.uiCPMW.lineEditLoopDelay.text()])
        elif self.uiCPMW.comboBoxTestType.currentText() == 'Signaling 1 and 2 not synchronously':
            QtGui.QMessageBox.information(self, 'Information:', 'This functionality will be enabled in the future.')
            return 'None'
        # return []
        # print('ok')

    def updateSign2Min(self):
        self.uiCPMW.lineEditMinSignSynch2.setText(self.uiCPMW.lineEditMaxSignSynch1.text())

    def updateSign2Max(self):
        self.uiCPMW.lineEditMaxSignSynch2.setText(self.uiCPMW.lineEditMinSignSynch1.text())


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
            # QtGui.QMessageBox.warning(self, 'Error!!!', 'Error during connection to CMW-500:\n' + str(e),
            #                           QtGui.QMessageBox.Ok)
            return ('Error during connection to CMW-500:\n' + str(e), self.connectWindow.text())

    @staticmethod
    def cmw_connect(parent=None):
        okno = Connection_Test(parent)
        okno.show()
        okno.find_resources()
        ok = okno.exec_()
        result, connect_addres = okno.start_test_connection()
        if ok == 0:
            return (result, connect_addres, ok == QtGui.QDialog.Rejected)
        elif ok == 1:
            return (result, connect_addres, ok == QtGui.QDialog.Accepted)


if __name__ == "__main__":

    cmw500 = QtGui.QApplication(sys.argv)
    cmw500Window = CMW500ManagerWindow()
    cmw500Window.show()
    sys.exit(cmw500.exec())