import customtkinter

from UI.widgets.date_picker import DatePicker
from PIL import Image


class DateEntry(customtkinter.CTkFrame):

    def __init__(self, parent, placeholder_text="", font=None, width=140, **kwargs):
        super().__init__(parent, width=width, **kwargs)

        self.entry = customtkinter.CTkEntry(self, placeholder_text=placeholder_text, font=font)
        self.entry.grid(row=0, column=0, padx=(3, 5), pady=3)

        self.date_picker = customtkinter.CTkButton(self, command=self.command_callback, text="", width=30, image=customtkinter.CTkImage(light_image=Image.open("UI/assets/date_picker.png")))
        self.date_picker.grid(row=0, column=1, padx=(0, 3), pady=3)

    def command_callback(self):
        date = DatePicker.get_date()
        self.entry.delete(0, "end")
        self.entry.insert(0, date.strftime("%d/%m/%Y"))







