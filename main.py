import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon
from gui import Ui_Dialog

class Main(QtWidgets.QMainWindow, Ui_Dialog):

    def __init__(self, dialog):
        super(Main, self).__init__(dialog)
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)

        self.unit_multiplier = 1
        self.progDir = os.path.dirname(os.path.realpath(__file__))

        self.icon = QtGui.QIcon(os.path.join(self.progDir + os.path.sep + 'ic.png'))
        self.menu = QtWidgets.QMenu()

        self.createInterface()

    def createInterface(self):
        dialog.setWindowIcon(QtGui.QIcon(self.progDir + os.path.sep + 'ic.png'))
        self.createSystemTrayIcon()
        # UI
        self.setBtn.clicked.connect(self.setBtn_clicked)
        self.radioButtons.clicked.connect(self.radBtn_s_clicked)
        self.radioButtonm.clicked.connect(self.radBtn_m_clicked)

    def createSystemTrayIcon(self):
        """
        Create a system tray icon with a context menu
        """
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.tray.setToolTip("Not Set")

        self.showAction = self.menu.addAction("Reset")
        self.showAction.triggered.connect(self.resetWindow)
        self.hideAction = self.menu.addAction("Hide")
        self.hideAction.triggered.connect(self.hideWindow)
        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(sys.exit)

    def radBtn_s_clicked(self):
        self.unit_multiplier = 1
        self.label_unit.setText('s')

    def radBtn_m_clicked(self):
        self.unit_multiplier = 60
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
            """
            time_secs = timer_input * self.unit_multiplier
            # print(time_secs)
            self.log.record_for(time_secs)
            a, m, k = self.log.session_stats()
            a = round(a, 2)
            ""
            self.tray.showMessage("Break Time!",
                                  "APM: " + str(a) + "  Mouse events: " + str(m) + " Keyboard events: " + str(k))
            ""
            self.label_dur.setText(str(timer_input) + " " + self.label_unit.text())
            self.label_apm.setText(str(a))
            self.label_ms.setText(str(m))
            self.label_kb.setText(str(k))
            """
            # dialog.resize(320, 320)
            # self.show()
            interval = 1000 * timer_input * self.unit_multiplier
            QtCore.QTimer.singleShot(interval, self.show)

            if self.unit_multiplier == 60:
                self.label_stat.setText(str(timer_input) + ' minutes(s) elapsed.  Take a Break! ')
            else:
                self.label_stat.setText(str(timer_input) + ' seconds elapsed.  Take a Break!')

            print(str(timer_input * self.unit_multiplier) + " s over ")

        except ValueError:
            # print("That's not an int!")
            self.label_stat.setText("That's not an integer")

    def show(self):
        dialog.show()

    def hideWindow(self):
        dialog.hide()

    def resetWindow(self):
        self.label_stat.setText("Reset")
        self.tray.setToolTip("")
        dialog.show()



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = Main(dialog)
    prog.show()

    sys.exit(app.exec_())
