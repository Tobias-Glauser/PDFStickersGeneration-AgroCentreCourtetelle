import customtkinter

from datetime import date as date_lib
from dateutil.relativedelta import relativedelta
import calendar as cal


class DatePicker:
    value = None

    @staticmethod
    def get_date():
        date_picker_window = DatePickerTopLevel(command=DatePicker.set_value)
        date_picker_window.wait_window()
        value = DatePicker.value
        DatePicker.value = None
        return value

    @staticmethod
    def set_value(value):
        DatePicker.value = value


class DatePickerTopLevel(customtkinter.CTkToplevel):

    def __init__(self, command=None, **kwargs):

        super().__init__(**kwargs)
        self.title("Sélectionner une date")
        self.after(250, lambda: self.iconbitmap("UI/assets/icon.ico"))

        if command is not None:
            self.command = command
        else:
            self.command = lambda ignored: None

        self.day_picker = DayPicker(self, command=self.command_callback)
        self.year_month_picker = YearMonthPicker(self, command=self.day_picker.update)
        self.year_month_picker.pack(padx=10, pady=10)
        self.day_picker.pack(padx=10, pady=10)

        self.today_button = customtkinter.CTkButton(self,
                                                    text="Aujourd'hui",
                                                    command=lambda: self.command_callback(date_lib.today()))
        self.today_button.pack(padx=10, pady=10)

        self.grab_set()

    def command_callback(self, date):
        self.command(date)
        self.destroy()


class YearMonthPicker(customtkinter.CTkFrame):

    def __init__(self, parent, start_date: date_lib = date_lib.today(), command=None, **kwargs):
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
        self.execute_command()

    def month_add(self):
        self.date = self.date + relativedelta(months=1)
        self.update()
        self.execute_command()

    def year_subtract(self):
        self.date = self.date - relativedelta(years=1)
        self.update()
        self.execute_command()

    def year_add(self):
        self.date = self.date + relativedelta(years=1)
        self.update()
        self.execute_command()

    def update(self):
        self.month.delete(0, "end")
        self.month.insert(0, self.date.strftime("%B"))
        self.year.delete(0, "end")
        self.year.insert(0, self.date.strftime("%Y"))

    def get_date(self):
        return self.date

    def execute_command(self):
        if self.command is not None:
            self.command(self.get_date())


class DayPicker(customtkinter.CTkFrame):

    def __init__(self, parent, date=None, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.date = None
        self.buttons = []

        if command is not None:
            self.command = command
        else:
            self.command = lambda ignored: None
        self.update(date)

    def update(self, actual_date: date_lib = None):
        self.date = actual_date
        if actual_date is None:
            self.date = date_lib.today()
        for button in self.buttons:
            button.destroy()

        calendar = cal.Calendar()
        month = calendar.monthdatescalendar(self.date.year, self.date.month)

        names = list(cal.day_name)
        for name in names:
            day_label = customtkinter.CTkLabel(self, text=name[:2], width=10, height=30)
            day_label.grid(row=0, column=names.index(name), padx=3, pady=3)

        for week in month:
            for day in week:
                button = customtkinter.CTkButton(self, text=str(day.day), command=lambda date=day: self.command(date),
                                                 width=30, height=30,
                                                 fg_color="#c20c20" if day.month != self.date.month else "#9c0c20",
                                                 hover_color="#9c0c20" if day.month != self.date.month else "#c20c20")
                button.grid(row=month.index(week) + 1, column=day.weekday(), padx=3, pady=3)
                self.buttons.append(button)
