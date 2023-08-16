import os
import win32print
import subprocess


class Printer:
    """
    Class for printing PDF files
    """
    def __init__(self, printer_name=None):
        """
        Printer class constructor
        :param printer_name: Name of the printer to use | None for default printer
        """
        self.foxit_path = os.getcwd().replace("\\", "\\\\") + "\\\\PDF-XChangeViewerPortable\\\\PDF" \
                                                              "-XChangeViewerPortable.exe"
        self.printer_name = None
        self.set_printer(printer_name)

    def set_printer(self, printer_name):
        """
        Sets the printer to use
        :param printer_name: Name of the printer to use | None for default printer
        :return: None
        """
        if printer_name is None or printer_name not in [p[2] for p in win32print.EnumPrinters(2)]:
            self.printer_name = win32print.GetDefaultPrinter()
        else:
            self.printer_name = printer_name

    def print(self, file_path):
        """
        Prints a pdf file
        :param file_path: Path to the pdf file to print
        :return: None
        :raises FileNotFoundError: If the file does not exist
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found: " + file_path)

        script = "\"" + \
                 self.foxit_path + \
                 "\" /printto:default=no \"" + \
                 self.printer_name + \
                 "\" \"" + \
                 file_path.replace("\\", "\\\\") + \
                 "\""
        subprocess.call(script, shell=True)
