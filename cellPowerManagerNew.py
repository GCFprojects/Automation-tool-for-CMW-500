from PyQt4.QtCore import QThread
import visa
import time


class CellPowerTest(QThread):

    def __init__(self, channel_to_test, connect_address='',
                 cell_test_loop=1, cell_test_loop_delay=1,

                 cell_1_power_min=-145, cell_1_power_max=-46,
                 cell_1_step=1, cell_1_time=1,

                 cell_2_power_min=-145, cell_2_power_max=-46,
                 cell_2_step=1, cell_2_time=1,

                 parent=None):

        super(CellPowerTest, self).__init__(parent)
        self.connect_address = connect_address
        self.rm = visa.ResourceManager()
        self.cmw_connection = self.rm.open_resource(self.connect_address)
        self.channel_to_test = channel_to_test
        self.cell_test_loop = cell_test_loop
        self.cell_test_loop_delay = cell_test_loop_delay

        if channel_to_test == '0' or channel_to_test == '1':
            self.cell_1_power_min = cell_1_power_min
            self.cell_1_power_max = cell_1_power_max
            self.cell_1_step = cell_1_step
            self.cell_1_time = cell_1_time

        if channel_to_test == '0' or channel_to_test == '2':
            self.cell_2_power_min = cell_2_power_min
            self.cell_2_power_max = cell_2_power_max
            self.cell_2_step = cell_2_step
            self.cell_2_time = cell_2_time

    def run(self):
        # print(self.connect_address)
        # self.connect_to_cmw()
        self.attenuation_test()

    def connect_to_cmw(self):
        print(self.cmw_connection.query("*IDN?"))
        self.cmw_connection.clear()
        self.cmw_connection.timeout = 2000
        self.cmw_connection.write("CONFigure:LTE:SIGN1:DL:PCC:RSEPre:LEVel?")
        print(self.cmw_connection.read())
        self.cmw_connection.clear()

    def attenuation_test(self):
        self.cmw_connection.clear()

        for i in range(int(self.cell_test_loop)):
            # Jeżeli user zaznaczył dwa kanały uruchom test '0'
            if self.channel_to_test == '0':
                cell_1_flag = float(self.cell_1_power_min)
                cell_2_flag = float(self.cell_2_power_min)

                steps_for_cell_1 = (float(self.cell_1_power_min) - float(self.cell_1_power_max)) / float(
                    self.cell_1_step)
                steps_for_cell_2 = (float(self.cell_2_power_min) - float(self.cell_2_power_max)) / float(
                    self.cell_2_step)
                if steps_for_cell_1 < 0:
                    steps_for_cell_1 = -steps_for_cell_1

                if steps_for_cell_2 < 0:
                    steps_for_cell_2 = -steps_for_cell_2

                if steps_for_cell_1 <= steps_for_cell_2:

                    if (self.cell_1_power_min <= self.cell_2_power_min) and \
                            (self.cell_1_power_max >= self.cell_2_power_max):
                        step = 1

                        for item in range(int(steps_for_cell_1 + 1)):
                            print('---------------Loop: ' + str(i + 1) + ' Step: ' + str(step) + '---------------')

                            self.manage_cell_1_power(cell_1_flag)
                            self.manage_cell_2_power(cell_2_flag)

                            cell_1_flag += float(self.cell_1_step)
                            cell_2_flag -= float(self.cell_2_step)
                            step += 1
                            time.sleep(float(self.cell_1_time))

                        cell_1_flag = float(self.cell_1_power_max)
                        cell_2_flag = float(self.cell_2_power_max)

                        for item in range(int(steps_for_cell_1 + 1)):
                            print('---------------Loop: ' + str(i + 1) + ' Step: ' + str(step) + '---------------')
                            self.manage_cell_1_power(cell_1_flag)
                            self.manage_cell_2_power(cell_2_flag)

                            cell_1_flag -= float(self.cell_1_step)
                            cell_2_flag += float(self.cell_2_step)
                            step += 1
                            time.sleep(float(self.cell_1_time))
                    elif (self.cell_1_power_min >= self.cell_2_power_min) and \
                            (self.cell_1_power_max <= self.cell_2_power_max):
                        step = 0
                        for item in range(int(steps_for_cell_1 + 1)):
                            print('---------------Loop: ' + str(i + 1) + ' Step: ' + str(step) + '---------------')

                            self.manage_cell_1_power(cell_1_flag)
                            self.manage_cell_2_power(cell_2_flag)

                            cell_1_flag -= float(self.cell_1_step)
                            cell_2_flag += float(self.cell_2_step)
                            step += 1
                            time.sleep(float(self.cell_1_time))

                        cell_1_flag = float(self.cell_1_power_max)
                        cell_2_flag = float(self.cell_2_power_max)

                        for item in range(int(steps_for_cell_1 + 1)):
                            print('---------------Loop: ' + str(i + 1) + ' Step: ' + str(step) + '---------------')
                            self.manage_cell_1_power(cell_1_flag)
                            self.manage_cell_2_power(cell_2_flag)

                            cell_1_flag += float(self.cell_1_step)
                            cell_2_flag -= float(self.cell_2_step)
                            step += 1
                            time.sleep(float(self.cell_1_time))
            # Jeżeli user zaznaczył tylko kanał pierwszy uruchom test '1'
            elif self.channel_to_test == '1':
                cell_1_flag = float(self.cell_1_power_min)
                item = 1

                while float(self.cell_1_power_min) <= cell_1_flag and float(self.cell_1_power_max) >= cell_1_flag:
                    print('--------------- Loop: ' + str(i+1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_1_power(cell_1_flag)

                    cell_1_flag = float(cell_1_flag) + float(self.cell_1_step)
                    item += 1
                    time.sleep(float(self.cell_1_time))

                while float(self.cell_1_power_min) >= cell_1_flag and float(self.cell_1_power_max) <= cell_1_flag:
                    print('--------------- Loop: ' + str(i + 1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_1_power(cell_1_flag)

                    cell_1_flag = float(cell_1_flag) - float(self.cell_1_step)
                    item += 1
                    time.sleep(float(self.cell_1_time))

                cell_1_flag = float(self.cell_1_power_max)
                while float(self.cell_1_power_min) <= cell_1_flag and float(self.cell_1_power_max) >= cell_1_flag:
                    print('--------------- Loop: ' + str(i+1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_1_power(cell_1_flag)

                    cell_1_flag = float(cell_1_flag) - float(self.cell_1_step)
                    item += 1
                    time.sleep(float(self.cell_1_time))

                while float(self.cell_1_power_min) >= cell_1_flag and float(self.cell_1_power_max) <= cell_1_flag:
                    print('--------------- Loop: ' + str(i+1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_1_power(cell_1_flag)

                    cell_1_flag = float(cell_1_flag) + float(self.cell_1_step)
                    item += 1
                    time.sleep(float(self.cell_1_time))
            # Jeżeli user zaznaczył tylko kanał drugi uruchom test '2'
            elif self.channel_to_test == '2':
                item = 1
                cell_2_flag = float(self.cell_2_power_min)

                while float(self.cell_2_power_min) <= cell_2_flag and float(self.cell_2_power_max) >= cell_2_flag:
                    print('--------------- Loop: ' + str(i+1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_2_power(cell_2_flag)

                    cell_2_flag = float(cell_2_flag) + float(self.cell_2_step)
                    item += 1
                    time.sleep(float(self.cell_2_time))

                while float(self.cell_2_power_min) >= cell_2_flag and float(self.cell_2_power_max) <= cell_2_flag:
                    print('--------------- Loop: ' + str(i + 1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_2_power(cell_2_flag)

                    cell_2_flag = float(cell_2_flag) - float(self.cell_2_step)
                    item += 1
                    time.sleep(float(self.cell_2_time))

                cell_2_flag = float(self.cell_2_power_max)
                while float(self.cell_2_power_min) <= cell_2_flag and float(self.cell_2_power_max) >= cell_2_flag:
                    print('--------------- Loop: ' + str(i+1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_2_power(cell_2_flag)

                    cell_2_flag = float(cell_2_flag) - float(self.cell_2_step)
                    item += 1
                    time.sleep(float(self.cell_2_time))

                while float(self.cell_2_power_min) >= cell_2_flag and float(self.cell_2_power_max) <= cell_2_flag:
                    print('--------------- Loop: ' + str(i+1) + ' Step: ' + str(item) + ' ---------------')
                    self.manage_cell_2_power(cell_2_flag)

                    cell_2_flag = float(cell_2_flag) + float(self.cell_2_step)
                    item += 1
                    time.sleep(float(self.cell_2_time))
        time.sleep(self.cell_test_loop_delay)

    def manage_cell_1_power(self, cell_1_flag):
        self.cmw_connection.timeout = 20000
        self.cmw_connection.write("CONFigure:LTE:SIGN1:DL:PCC:RSEPre:LEVel " + str(cell_1_flag))
        self.cmw_connection.write("CONFigure:LTE:SIGN1:DL:PCC:RSEPre:LEVel?")
        print('Channel 1: ' + self.cmw_connection.read() + ' [dBm]')  # Wyślij do okna logowania
        self.cmw_connection.clear()

    def manage_cell_2_power(self, cell_2_flag):
        self.cmw_connection.timeout = 20000
        self.cmw_connection.write("CONFigure:LTE:SIGN2:DL:PCC:RSEPre:LEVel " + str(cell_2_flag))
        self.cmw_connection.write("CONFigure:LTE:SIGN2:DL:PCC:RSEPre:LEVel?")
        print('Channel 2: ' + self.cmw_connection.read() + ' [dBm]')  # Wyślij do okna logowania
        self.cmw_connection.clear()
