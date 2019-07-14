from os import path, makedirs as os_makedirs
from time import sleep as tsleep, time as current_time
import csv
from datetime import datetime
import pyHook
import pythoncom


class Log:

    def __init__(self):
        # print("  log init ")
        self.running = False
        self.mouse_event_count = 0
        self.kb_event_count = 0
        self.rem_time_secs = 0.5

        self.subdir_month = datetime.now().strftime("%Y-%m")
        self.date_today = datetime.now().strftime("%Y-%m-%d")
        self.subdir = path.join('.' + path.sep + 'stats', self.subdir_month)
        self.file_path_stats_today = path.join('.' + path.sep + 'stats', self.subdir_month,
                                                  self.date_today + '.csv')


    # -------------------------------------------------------------------------------------------------------------------
    def OnMouseEvent(self, event):

        self.mouse_event_count += 1
        # print('Message id:' + " " + str(event.Message) + " " + datetime.now().time().strftime('%H:%M:%S'))
        # print('MessageName:' + " " + str(event.MessageName))

        logFile = path.join('.' + path.sep + 'stats', 'last_session_events.csv')
        with open(logFile, 'a', newline='') as myFile:
            writer = csv.writer(myFile, delimiter=',')
            writer.writerow([datetime.now().time().strftime('%H:%M:%S'), str(event.Message), str(event.MessageName)])
        # print('---')
        return True

    def OnKeyboardEvent(self, event):

        self.kb_event_count += 1
        # print('Message id:' + " " + str(event.Message) + " " + datetime.now().time().strftime('%H:%M:%S'))
        # print('MessageName:' + " " + str(event.MessageName))

        logFile = path.join('.' + path.sep + 'stats', 'last_session_events.csv')
        with open(logFile, 'a', newline='') as myFile:
            writer = csv.writer(myFile, delimiter=',')
            writer.writerow([datetime.now().time().strftime('%H:%M:%S'), str(event.Message), str(event.MessageName)])
        # print('---')
        return True

    # ------------------------------------------------------------------------------------------------------------------

    def record_for(self, secs_to_run):
        self.rem_time_secs = secs_to_run
        self.mouse_event_count = 0
        self.kb_event_count = 0

        self.session_file_start(str(self.rem_time_secs) + " s")

        hm = pyHook.HookManager()
        hm.MouseWheel = self.OnMouseEvent
        hm.MouseAllButtonsDown = self.OnMouseEvent
        hm.KeyUp = self.OnKeyboardEvent

        hm.HookMouse()
        hm.HookKeyboard()
        # print("--hook-- for " + str(self.rem_time_secs))

        timeout = current_time() + self.rem_time_secs
        while current_time() < timeout:
            pythoncom.PumpWaitingMessages()
            tsleep(0.001)

        # print(self.mouse_event_count)
        # print(self.kb_event_count)

        hm.UnhookMouse()
        hm.UnhookKeyboard()
        # print('---unhook---')

        self.session_save_stats(str(self.rem_time_secs))

    def manual_record_start(self):

        self.session_file_start("manual mode")

        hm = pyHook.HookManager()
        hm.MouseWheel = self.OnMouseEvent
        hm.MouseAllButtonsDown = self.OnMouseEvent
        hm.KeyUp = self.OnKeyboardEvent

        hm.HookMouse()
        hm.HookKeyboard()
        # print("--hook-- manual ")
        self.mouse_event_count = 0
        self.kb_event_count = 0

        self.running = True
        time_in = current_time()
        while self.running:
            pythoncom.PumpWaitingMessages()
            tsleep(0.001)

        hm.UnhookMouse()
        hm.UnhookKeyboard()
        self.rem_time_secs = round(current_time() - time_in, 2)
        print('---unhook---')
        self.session_save_stats("~"+str(self.rem_time_secs))

    def manual_record_stop(self):
        self.running = False


    def session_file_start(self, duration_str):
        """
                            creates subdir for today if not exists
                            start temporary log file for all events in the session
        """
        if self.date_today != datetime.now().strftime("%Y-%m-%d"):
            self.subdir_month = datetime.now().strftime("%Y-%m")
            self.date_today = datetime.now().strftime("%Y-%m-%d")

            self.subdir = path.join('.' + path.sep + 'stats', self.subdir_month)
            self.file_path_stats_today = path.join('.' + path.sep + 'stats', self.subdir_month,
                                                      self.date_today + '.csv')

        if not path.exists(self.subdir):
            try:
                os_makedirs(self.subdir)
            except Exception:
                print("Can't create stats folder ")

        logfile = path.join('.' + path.sep + 'stats', 'last_session_events.csv')
        with open(logfile, 'w', newline='') as myFile:
            writer = csv.writer(myFile, delimiter=',')
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), duration_str, "Session started"])

    # print("Writing complete")

    def session_save_stats(self, duration_str):
        """
                            append session stats to file_path_stats_today
                            format: datetime, time interval, ms events, kb events
        """

        with open(self.file_path_stats_today, 'a', newline='') as stats_file:
            writer = csv.writer(stats_file, delimiter=',')
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), duration_str, str(self.mouse_event_count),
                             str(self.kb_event_count)])

    # print("Stats saved", str(self.rem_time_secs))

    def session_stats(self):
        total = self.kb_event_count + self.mouse_event_count
        apm = (total * 60) / self.rem_time_secs
        return (apm, self.mouse_event_count, self.kb_event_count)

    # -------------------------------------------------------------------------------------------------------------------


"""
l = logg()  # type: logg
l.fors(20)
"""
