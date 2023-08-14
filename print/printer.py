import os
import win32print
import subprocess


class Printer:
    def __init__(self, printer_name=None):
        self.foxit_path = os.getcwd().replace("\\", "\\\\") + "\\\\PDF-XChangeViewerPortable\\\\PDF" \
                                                              "-XChangeViewerPortable.exe"
        self.printer_name = None
        self.set_printer(printer_name)

    def set_printer(self, printer_name):
        if printer_name is None or printer_name not in [p[2] for p in win32print.EnumPrinters(2)]:
            self.printer_name = win32print.GetDefaultPrinter()
        else:
            self.printer_name = printer_name

    def print(self, file_path):
        script = "\"" + \
                 self.foxit_path + \
                 "\" /printto:default=no \"" + \
                 self.printer_name + \
                 "\" \"" + \
                 file_path.replace("\\", "\\\\") + \
                 "\""
        subprocess.call(script, shell=True)
