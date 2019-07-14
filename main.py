import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon
"""
import profile
import cProfile, pstats, io
import time

py -m cProfile mainc.py

"""
from gui import Ui_Dialog
import logger_win32


class Main(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self, dialog):
        super(Main, self).__init__(dialog)
        Ui_Dialog.__init__(self)

        self.log = logger_win32.Log() # log input events and active window title
        self.unit_multiplier = 1
        self.unit_multiplier_minutes = 60
        self.progDir = os.path.dirname(os.path.realpath(__file__))

        self.pm_is_working = False
        self.pm_qtimer = QtCore.QTimer(self)
        self.pm_qtimer.timeout.connect(self.pm_timer_display_timeout)
        self.pm_secs_left_int = 0

        self.setupUi(dialog)
        self.icon = QtGui.QIcon(os.path.join(self.progDir + os.path.sep + 'ic.png'))
        self.menu = QtWidgets.QMenu()

        self.createInterface()

    def createInterface(self):
        # dialog.setWindowIcon(QtGui.QIcon(self.progDir + os.path.sep + 'ic.png'))
        self.createSystemTrayIcon()
        # UI
        self.setBtn.clicked.connect(self.setBtn_clicked)
        self.radioButtons.clicked.connect(self.radBtn_s_clicked)
        self.radioButtonm.clicked.connect(self.radBtn_m_clicked)

        # ------------------------------------------------------------------------------
        self.tabWidget.currentChanged.connect(self.onTabChange)

        self.checkBox_mm_2.stateChanged.connect(self.manualMonitor)

        self.pushButton_pm_work.clicked.connect(self.pm_work_clicked)
        self.pushButton_pm_break.clicked.connect(self.pm_break_clicked)
        self.pushButton_pm_reset.clicked.connect(self.pm_reset_clicked)

        self.pushButton_pm_break.setGeometry(QtCore.QRect(120, 65, 0, 23))
        self.pushButton_pm_work.setGeometry(QtCore.QRect(120, 65, 80, 23))

    def createSystemTrayIcon(self):
        """Create a sys tray icon with a context menu"""

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.tray.setToolTip("Not Set")

        self.showAction = self.menu.addAction("Reset")
        self.showAction.triggered.connect(self.resetWindow)
        self.hideAction = self.menu.addAction("Hide")
        self.hideAction.triggered.connect(self.minimzeWindow)
        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(sys.exit)

    def onTabChange(self):
        """ for debugging"""
        print(self.tabWidget.currentIndex())
        """
        if self.tabWidget.currentIndex() == 0:
            pass
        """


    """ 
    pm = pomodoro mode
    
    
    """
    def pm_timer_display_start(self, seconds_int):
        self.pm_secs_left_int = seconds_int
        self.pm_qtimer.start(1000*self.unit_multiplier_minutes)
        self.pm_update_gui_timer()

    def pm_timer_display_timeout(self):
        self.pm_secs_left_int -= 1

        if self.pm_secs_left_int <= 0:
            self.label_stat.setText("Time over!")
            self.pm_qtimer.stop()
            if self.pm_is_working:
                self.tray.showMessage("Pomodoro", "Session Complete \nTake a short break")
                self.pushButton_pm_work.setGeometry(QtCore.QRect(120, 65, 0, 23))
                self.pushButton_pm_break.setGeometry(QtCore.QRect(120, 65, 80, 23))
            else:
                self.pushButton_pm_break.setGeometry(QtCore.QRect(120, 65, 0, 23))
                self.pushButton_pm_work.setGeometry(QtCore.QRect(120, 65, 80, 23))

        else:
            self.pm_update_gui_timer()

    def pm_update_gui_timer(self):
        self.label_stat.setText(str(self.pm_secs_left_int) + ' minute(s) left')

    def pm_work_clicked(self):
        print("pm_work_clicked")
        try:
            pm_timer_input = int(self.lineEdit_pm_work.text())
            self.pm_timer_display_start(pm_timer_input)

            self.pushButton_pm_work.setGeometry(QtCore.QRect(120, 65, 0, 23))
            self.pm_is_working = True

        except ValueError:
            # print("That's not an int!")
            self.label_stat.setText("That's not a valid input")

    def pm_break_clicked(self):
        try:
            pm_timer_input = int(self.lineEdit_pm_break.text())
            self.pm_timer_display_start(pm_timer_input)

            self.pushButton_pm_break.setGeometry(QtCore.QRect(120, 65, 0, 23))
            self.pm_is_working = False

        except ValueError:
            # print("That's not an int!")
            self.label_stat.setText("That's not a valid input")

    def pm_reset_clicked(self):
        try:
            self.pm_qtimer.stop()
            self.label_stat.setText("Reset")
            self.pushButton_pm_work.setGeometry(QtCore.QRect(120, 65, 80, 23))
            self.pushButton_pm_break.setGeometry(QtCore.QRect(120, 65, 0, 23))
        except AttributeError:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def manualMonitor(self, state):
        if state == QtCore.Qt.Checked:
            print('mm checked')
            self.startMon()

        else:
            print('mm Unchecked')
            self.stopMon()

    def startMon(self):
        self.tray.setToolTip("Mon Running..")
        self.label_stat.setText("Manual activity monitor is running")
        self.log.manual_record_start()

    def stopMon(self):
        self.tray.setToolTip("Mon Stopped.")
        self.label_stat.setText("Manual activity monitor has been stopped")
        self.log.manual_record_stop()

        a, m, k = self.log.session_stats()
        a = round(a, 2)

        self.label_dur.setText("manual")
        self.label_apm.setText(str(a))
        self.label_ms.setText(str(m))
        self.label_kb.setText(str(k))

    def radBtn_s_clicked(self):
        self.unit_multiplier = 1
        self.label_unit.setText('s')

    def radBtn_m_clicked(self):
        self.unit_multiplier = self.unit_multiplier_minutes
        self.label_unit.setText('min')

    def setBtn_clicked(self):
        self.label_stat.setText('Time set to ' + self.lineEdit.text())
        try:
            timer_input = float(self.lineEdit.text())
            timer_input = round(timer_input, 2)
            # self.label_stat.setText(self.lineEdit.text() + " " + self.label_unit.text() + ' elapsed ')
            dialog.hide()

            self.tray.setToolTip(str(timer_input) + " " + self.label_unit.text())
            """
            self.tray.showMessage("Reminder", "Timer set to " + str(timer_input) + " " + self.label_unit.text())
            """
            time_secs = timer_input * self.unit_multiplier
            # print(time_secs)
            self.log.record_for(time_secs)
            a, m, k = self.log.session_stats()
            a = round(a, 2)
            """
            self.tray.showMessage("Break Time!",
                                  "APM: " + str(a) + "  Mouse events: " + str(m) + " Keyboard events: " + str(k))
            """
            self.label_dur.setText(str(timer_input) + " " + self.label_unit.text())
            self.label_apm.setText(str(a))
            self.label_ms.setText(str(m))
            self.label_kb.setText(str(k))

            dialog.resize(320, 320)
            self.show()
            interval = 1000 * timer_input * self.unit_multiplier
            # QtCore.QTimer.singleShot(interval, self.show)

            if self.unit_multiplier == self.unit_multiplier_minutes:
                self.label_stat.setText(str(timer_input) + ' minutes(s) elapsed.  Take a Break! ')
            else:
                self.label_stat.setText(str(timer_input) + ' seconds elapsed.  Take a Break!')

            # print(str(timer_
            # input * self.unit_multiplier) + " s over ")

        except ValueError:
            # print("That's not an int!")
            self.label_stat.setText("That's not an integer")

    def show(self):
        dialog.show()

    def minimzeWindow(self):
        dialog.hide()

    def resetWindow(self):
        self.pm_reset_clicked()
        self.label_stat.setText("Reset")
        self.tray.setToolTip("")
        dialog.show()

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    # print("App is running")
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = Main(dialog)
    dialog.resize(330, 280)
    dialog.show()

    sys.exit(app.exec_())

# profile.run('main()')








