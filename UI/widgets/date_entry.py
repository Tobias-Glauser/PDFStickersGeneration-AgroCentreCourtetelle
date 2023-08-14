import customtkinter

from UI.widgets.date_picker import DatePicker
from PIL import Image


class DateEntry(customtkinter.CTkFrame):

    def __init__(self, parent, placeholder_text="", font=None, width=140, height=28, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(1, weight=0)  # buttons don't expand
        self.grid_columnconfigure(0, weight=1)  # entry expands

        self.entry = customtkinter.CTkEntry(self, placeholder_text=placeholder_text, width=width-36-5, height=height, font=font)
        self.entry.grid(row=0, column=0, padx=(0, 5), pady=0)

        button_size = height
        self.date_picker = customtkinter.CTkButton(self, command=self.command_callback, text="", width=button_size, height=button_size, image=customtkinter.CTkImage(light_image=Image.open("UI/assets/date_picker.png"), size=(20, 20)))
        self.date_picker.grid(row=0, column=1, padx=(0, 0), pady=0)

    def command_callback(self):
        date = DatePicker.get_date()
        if date is not None:
            self.entry.delete(0, "end")
            self.entry.insert(0, date.strftime("%d/%m/%Y"))

    def get(self):
        return self.entry.get()







