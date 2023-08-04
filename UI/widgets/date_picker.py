import customtkinter
from datetime import date
from dateutil.relativedelta import relativedelta


class DatePicker(customtkinter.CTkFrame):

    def __init__(self, parent, **kwargs):

        super().__init__(parent, **kwargs)
        self.year_month_picker = YearMonthPicker(self)
        self.year_month_picker.pack(side="left", fill="both", expand=True)


class YearMonthPicker(customtkinter.CTkFrame):

    def __init__(self, parent, start_date: date = date.today(), command=None, **kwargs):

        super().__init__(parent, **kwargs)
        self.date = start_date
        self.command = command

        self.month_substract_button = customtkinter.CTkButton(self, text="<", command=self.month_subtract, width=20)
        self.month_substract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.month = customtkinter.CTkEntry(self, width=80, height=10, border_width=0)
        self.month.grid(row=0, column=1, padx=3, pady=3)
        self.month_add_button = customtkinter.CTkButton(self, text=">", command=self.month_add, width=20)
        self.month_add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.year_substract_button = customtkinter.CTkButton(self, text="<", command=self.year_subtract, width=20)
        self.year_substract_button.grid(row=0, column=3, padx=(3, 0), pady=3)
        self.year = customtkinter.CTkEntry(self, width=80, height=10, border_width=0)
        self.year.grid(row=0, column=4, padx=3, pady=3)
        self.year_add_button = customtkinter.CTkButton(self, text=">", command=self.year_add, width=20)
        self.year_add_button.grid(row=0, column=5, padx=(0, 3), pady=3)

        self.update()

    def month_subtract(self):
        self.date = self.date - relativedelta(months=1)
        self.update()
        self.command(self.get_date())

    def month_add(self):
        self.date = self.date + relativedelta(months=1)
        self.update()
        self.command(self.get_date())

    def year_subtract(self):
        self.date = self.date - relativedelta(years=1)
        self.update()
        self.command(self.get_date())

    def year_add(self):
        self.date = self.date + relativedelta(years=1)
        self.update()
        self.command(self.get_date())

    def update(self):
        self.month.delete(0, "end")
        self.month.insert(0, self.date.strftime("%B"))
        self.year.delete(0, "end")
        self.year.insert(0, self.date.strftime("%Y"))

    def get_date(self):
        return self.date


# class DayPicker(customtkinter.CTkFrame):
#
#     def __init__(self, parent, date=None, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.date = None
#         self.update(date)
#         self.buttons = []
#
#     def update(self, date=None):
#         self.date = date
#         for button in self.buttons:
#             button.destroy()
#
#
#
#

