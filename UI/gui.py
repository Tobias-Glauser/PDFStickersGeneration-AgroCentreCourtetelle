import os.path
import time
import win32print
from threading import Thread

import customtkinter
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox

from UI.widgets.date_entry import DateEntry
from UI.widgets.pdf_gen_progress_bar import StickerGenProgressBar
from UI.widgets.int_spinbox import IntSpinbox
from sticker.sticker_data import StickerDataNumber, StickerDataText, StickerDataDate, StickerDataList
from print.printer import Printer

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("UI/theme/agrocentre.json")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    """
    Class to represent the main application
    """
    sticker_frame = None

    def __init__(self, stickers):
        """
        App constructor
        :param stickers: Stickers object that contains all the stickers
        :return: None
        """
        super().__init__()
        self.button = None
        self.stickers = stickers
        self.geometry("500x480")
        self.title("Sticker - AGROCENTRE & KILOMETRE ZERO")
        self.iconbitmap("UI/assets/icon.ico")
        self.thread = None
        # self.resizable(False, False)

        self.printer = Printer()

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure((0, 1), weight=1)

        self.labelConfig = customtkinter.CTkLabel(self, text="Config stickers", font=("Calibri", 30), height=40)
        self.labelConfig.grid(row=0, column=0, columnspan=1, padx=10, pady=10)

        self.config_sticker_frame = ConfigStickerFrame(self)
        self.config_sticker_frame.grid(row=1, column=0, columnspan=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self, text="Type d'autocollant", font=("Calibri", 30), height=40)
        self.label.grid(row=0, column=1, columnspan=1, padx=10, pady=10)

        self.combobox_stickers = customtkinter.CTkComboBox(self, values=(self.stickers.get_stickers_values()),
                                                           command=self.display_sticker, font=("Calibri", 24),
                                                           dropdown_font=("Calibri", 24), width=280)
        self.combobox_stickers.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

        self.printer_choice_frame = PrinterChoiceFrame(self, self.set_printer)
        self.printer_choice_frame.grid(row=5, column=0, columnspan=1, rowspan=1, sticky="nsew", padx=10, pady=10)

    def display_sticker(self, choice):
        """
        Display the sticker
        :param choice: Name of the sticker to display
        :return: None
        """
        if self.stickers.selected_sticker is not None and choice == self.stickers.selected_sticker.name:
            return
        if self.sticker_frame is not None:
            self.sticker_frame.destroy()
            self.sticker_frame.pack_forget()
        self.stickers.selected_sticker = next(
            sticker for sticker in self.stickers.stickers_list if sticker.name == choice)
        self.sticker_frame = StickerFrame(self, self.stickers.selected_sticker)
        self.sticker_frame.grid(row=2, column=1, columnspan=1, rowspan=10, sticky="nsew", padx=10, pady=10)

        self.button = customtkinter.CTkButton(self,
                                              text="Générer",
                                              command=lambda: self.generate_sticker_callback(self.sticker_frame))
        self.button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

        self.button = customtkinter.CTkButton(self,
                                              text="Imprimer",
                                              command=lambda: self.print_sticker_callback(self.sticker_frame))
        self.button.grid(row=6, column=0, columnspan=1, padx=10, pady=10)

    def generate_sticker_callback(self, sticker_frame):
        """
        Callback for the generate button
        :param sticker_frame: Frame that contains the sticker fields
        :return: None
        """
        if self.thread is not None and self.thread.is_alive():
            CTkMessagebox(title="Error", message="Il y a dejà un sticker en cours de création", icon="cancel")
            return

        self.thread = Thread(target=self.generate_sticker_generate_method, args=(sticker_frame,)).start()

    def generate_sticker_generate_method(self, sticker_frame):
        """
        Generate the sticker with the generate method (no printing)
        :param sticker_frame: Frame that contains the sticker fields
        :return: None
        """
        result = self.generate_sticker(sticker_frame)
        if result is False:
            return

        os.startfile(result)

    def print_sticker_callback(self, sticker_frame):
        """
        Callback for the print button
        :param sticker_frame: Frame that contains the sticker fields
        :return: None
        """
        if self.thread is not None and self.thread.is_alive():
            CTkMessagebox(title="Error", message="Il y a dejà un sticker en cours de création", icon="cancel")
            return

        self.thread = Thread(target=self.generate_sticker_print_method, args=(sticker_frame,)).start()

    def generate_sticker_print_method(self, sticker_frame):
        """
        Generate the sticker with the print method (printing)
        :param sticker_frame: Frame that contains the sticker fields
        :return: None
        """
        filename = os.getcwd() + "\\tmp\\tmp_1.pdf"
        while os.path.exists(filename):
            number = (filename.split(".")[0]).split("_")[-1]
            filename = filename.replace(number, str(int(number) + 1))
        result = self.generate_sticker(sticker_frame, filename)
        if result is False:
            return

        Thread(target=self.printer.print, args=(result,)).start()

    def print_sticker(self, file_path):
        """
        Print the sticker
        :param file_path: path to the sticker pdf file
        :return: None
        """
        self.printer.print(file_path)
        time.sleep(60)
        os.remove(file_path)

    def generate_sticker(self, sticker_frame, save_file_path=None):
        """
        Generate the sticker
        :param sticker_frame: Frame that contains the sticker fields
        :param save_file_path: Path to save the sticker to
        :return: Path to the sticker pdf file if it was generated, False otherwise
        """
        sticker_frame.get_data()

        if not sticker_frame.sticker.is_valid():
            CTkMessagebox(title="Erreur",
                          message="Les champs ne sont pas tous remplis ou correctement remplis.",
                          icon="cancel")
            return False

        stickers_left, total_stickers = self.config_sticker_frame.get_data()
        if stickers_left == "" or stickers_left is None:
            msg = CTkMessagebox(title="Attention !",
                                message="Comme vous n'avez pas inscrit le nombre de stickers restants, le nombre de "
                                        "stickers restants sera égal au nombre de stickers qui se trouvent sur une "
                                        "page",
                                icon="warning",
                                option_1="Continuer",
                                option_2="Annuler")
            if msg.get() == "Annuler":
                return False
            else:
                stickers_left = 0
        elif stickers_left > 24:
            msg = CTkMessagebox(title="Attention !",
                                message="Le nombre de stickers restants est supérieur à 24, êtes-vous sûr de vouloir "
                                        "continuer ?",
                                icon="warning",
                                option_1="Continuer",
                                option_2="Annuler")
            if msg.get() == "Annuler":
                return False
            else:
                stickers_left = 0

        if total_stickers == "" or total_stickers is None:
            msg = CTkMessagebox(title="Attention !",
                                message="Comme vous n'avez pas inscrit le nombre de sticker désirés, le nombre de "
                                        "stickers désirés sera égal au nombre de stickers qui se trouvent sur une page",
                                icon="warning",
                                option_1="Continuer",
                                option_2="Annuler")
            if msg.get() == "Annuler":
                return False
            else:
                total_stickers = 24

        if total_stickers < 1:
            CTkMessagebox(title="Erreur",
                          message="Le nombre de stickers désirés doit être supérieur à 0.",
                          icon="cancel")
            return False

        if stickers_left < 0:
            CTkMessagebox(title="Erreur",
                          message="Le nombre de stickers restants doit être supérieur ou égal à 0.",
                          icon="cancel")
            return False

        if save_file_path is None:
            save_file_path = filedialog.asksaveasfilename(filetypes=[("PDF", "*.pdf")],
                                                          defaultextension=".pdf",
                                                          initialfile=sticker_frame.sticker.name + " 1.pdf")

        if not os.path.exists(os.path.dirname(save_file_path)):
            return False

        progress_bar = StickerGenProgressBar(self, width=50)
        progress_bar.grid(row=4, column=0, columnspan=1, padx=10, pady=10, sticky="ew")
        self.update()
        try:
            sticker_frame.sticker.generate(save_file_path,
                                           progress_bar.set_state,
                                           stickers_left=stickers_left,
                                           total_stickers=total_stickers)
        except Exception as e:
            if e.args[0] == "Line too long":
                CTkMessagebox(title="Erreur",
                              message="Le texte du champ " + e.args[1] + " (" + e.args[2] + ") est trop long pour "
                                                                                            "l'autocollant.",
                              icon="cancel")
            progress_bar.destroy()
            return False
        progress_bar.destroy()
        self.empty_sticker_page_config_fields()
        return save_file_path

    def set_printer(self, _ignored):
        """
        Set the printer to use
        :param _ignored: Unused parameter
        :return: None
        """
        self.printer.set_printer(self.printer_choice_frame.get_printer())

    def empty_sticker_page_config_fields(self):
        """
        Empty the sticker page config fields
        :return: None
        """
        self.config_sticker_frame.stickers_left.empty()
        self.config_sticker_frame.total_stickers.empty()


class StickerFrame(customtkinter.CTkScrollableFrame):
    """
    Class to represent the frame that contains the sticker fields
    """
    def __init__(self, parent, sticker, **kwargs):
        """
        StickerFrame constructor
        :param parent: Parent frame
        :param sticker: Sticker to display
        :param kwargs: Keyword arguments for the customtkinter.CTkScrollableFrame class
        """
        super().__init__(parent, **kwargs, height=340)
        self.sticker = sticker
        self.entries = []

        for data in self.sticker.data:
            if isinstance(data, StickerDataText):
                customtkinter.CTkLabel(self, text=data.name, font=("Calibri", 14)).pack(pady=0, padx=10, expand=False,
                                                                                        anchor="w")
                entry = customtkinter.CTkEntry(self, placeholder_text=data.name, width=280, font=("Calibri", 14))
                entry.pack(pady=(0, 10), padx=10)
                self.entries.append({
                    'entry': entry,
                    'data': data})
            elif isinstance(data, StickerDataNumber):
                customtkinter.CTkLabel(self, text=data.name, font=("Calibri", 14)).pack(pady=0, padx=10, expand=False,
                                                                                        anchor="w")
                entry = customtkinter.CTkEntry(self, placeholder_text=data.name,  width=280, font=("Calibri", 14))
                entry.pack(pady=(0, 10), padx=10)
                self.entries.append({
                    'entry': entry,
                    'data': data})
            elif isinstance(data, StickerDataDate):
                customtkinter.CTkLabel(self, text=data.name, font=("Calibri", 14)).pack(pady=0, padx=10, expand=False,
                                                                                        anchor="w")
                entry = DateEntry(self, placeholder_text=data.name, width=280, font=("Calibri", 14))
                entry.pack(pady=(0, 10), padx=10)
                self.entries.append({
                    'entry': entry,
                    'data': data})
            elif isinstance(data, StickerDataList):
                customtkinter.CTkLabel(self, text=data.name, font=("Calibri", 14)).pack(pady=0, padx=10, expand=False,
                                                                                        anchor="w")
                entry = customtkinter.CTkComboBox(self, values=data.values, width=280, font=("Calibri", 14),
                                                  dropdown_font=("Calibri", 14))
                entry.pack(pady=(0, 10), padx=10)
                entry.set(data.values[0])
                self.entries.append({
                    'entry': entry,
                    'data': data})

    def get_data(self):
        """
        Put the data from the entry fields into the sticker data
        :return: None
        """
        for thing in self.entries:
            if isinstance(thing['data'], StickerDataText):
                thing['data'].value = thing['entry'].get()
            elif isinstance(thing['data'], StickerDataNumber):
                thing['data'].value = thing['entry'].get()
            elif isinstance(thing['data'], StickerDataDate):
                thing['data'].value = thing['entry'].get()
            elif isinstance(thing['data'], StickerDataList):
                thing['data'].value = thing['entry'].get()

    def scroll_end(self):
        """
        Scroll to the end of the frame
        :return: None
        """
        self._parent_canvas.yview("scroll", 100000, "units")
        self.update()


class ConfigStickerFrame(customtkinter.CTkFrame):
    """
    Class to represent the frame that contains the sticker page config fields
    """
    def __init__(self, parent, **kwargs):
        """
        ConfigStickerFrame constructor
        :param parent: Parent frame
        :param kwargs: Keyword arguments for the customtkinter.CTkFrame class
        :return: None
        """
        super().__init__(parent, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0 | 1), weight=1)

        self.label_stickers_left = customtkinter.CTkLabel(self, text="Stickers restants", font=("Calibri", 14))
        self.label_stickers_left.grid(row=0, column=0, pady=0, padx=10)
        self.stickers_left = IntSpinbox(self, width=150, step_size=1)
        self.stickers_left.grid(row=1, column=0, pady=0, padx=10, sticky="nsew")
        self.label_total_stickers = customtkinter.CTkLabel(self, text="Nombre de stickers", font=("Calibri", 14))
        self.label_total_stickers.grid(row=2, column=0, pady=0, padx=10)
        self.total_stickers = IntSpinbox(self, width=150, step_size=1)
        self.total_stickers.grid(row=3, column=0, pady=0, padx=10, sticky="nsew")

    def get_data(self):
        """
        Get the data from the sticker page config fields
        :return: A tuple containing the stickers left and the total stickers
        """
        return self.stickers_left.get(), self.total_stickers.get()


class PrinterChoiceFrame(customtkinter.CTkFrame):
    """
    Class to represent the frame that contains the printer choice field
    """
    def __init__(self, parent, command=None, **kwargs):
        """
        PrinterChoiceFrame constructor
        :param parent: Parent frame
        :param command: Command to execute when the printer is changed
        :param kwargs: Keyword arguments for the customtkinter.CTkFrame class
        """
        super().__init__(parent, **kwargs)

        self.label_printer_choice = customtkinter.CTkLabel(self, text="Imprimante", font=("Calibri", 14))
        self.label_printer_choice.pack(pady=0, padx=10, expand=False)
        self.printer_choice = customtkinter.CTkComboBox(self,
                                                        values=[p[2] for p in win32print.EnumPrinters(2)],
                                                        font=("Calibri", 14),
                                                        command=command)
        self.printer_choice.pack(pady=(0, 10), padx=10)
        self.printer_choice.set(win32print.GetDefaultPrinter())

    def get_printer(self):
        """
        Get the printer to use
        :return: The printer to use if it exists, None otherwise
        """
        choice = self.printer_choice.get()
        if choice in [p[2] for p in win32print.EnumPrinters(2)]:
            return choice
        return None
