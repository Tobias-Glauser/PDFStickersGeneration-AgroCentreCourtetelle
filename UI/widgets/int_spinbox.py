import time
from typing import Callable, Union

import customtkinter
from threading import Thread, Event


class IntSpinbox(customtkinter.CTkFrame):
    """
    Class to represent an integer spinbox
    """
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int] = 1,
                 command: Callable = None,
                 **kwargs):
        """
        IntSpinbox constructor
        :param args: Arguments for the customtkinter.CTkFrame class
        :param width: Width of the spinbox
        :param height: Height of the spinbox
        :param step_size: Increment or decrement value
        :param command: Command to execute when the value is changed
        :param kwargs: Keyword arguments for the customtkinter.CTkFrame class
        :return: None
        """
        super().__init__(*args, width=width, height=height, **kwargs)

        self.event = Event()
        self.timer = Thread(target=self.mouse_hold, args=(self.event,))
        self.holding = False

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0 | 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                                       command=self.on_press_substract)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.subtract_button.bind("<ButtonRelease-1>", self.on_release_substract)

        self.entry = customtkinter.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                                  command=self.on_press_add)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.add_button.bind("<ButtonRelease-1>", self.on_release_add)

        # default value
        self.entry.insert(0, "")

    def add_button_callback(self):
        """
        Callback for the add button
        :return: None
        """
        if self.command is not None:
            self.command()
        try:
            if self.entry.get() == "":
                self.entry.insert(0, 0)
                return
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        """
        Callback for the subtract button
        :return: None
        """
        if self.command is not None:
            self.command()
        if self.entry.get() == "":
            self.entry.insert(0, 0)
            return
        if int(self.entry.get()) <= 0:
            return
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        """
        Get the value of the entry field
        :return: The value of the entry field
        """
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        """
        Set the value of the entry field
        :param value: Integer value to set
        :return: None
        """
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))

    def empty(self):
        """
        Empty the entry field
        :return: None
        """
        self.entry.delete(0, "end")

    def on_press_add(self):
        """
        When the add button is pressed
        :return: None
        """
        self.event.clear()
        self.timer = Thread(target=self.mouse_hold, args=(self.event, self.add_button_callback))
        self.timer.start()

    def on_press_substract(self):
        """
        When the subtract button is pressed
        :return: None
        """
        self.event.clear()
        self.timer = Thread(target=self.mouse_hold, args=(self.event, self.subtract_button_callback))
        self.timer.start()

    def on_release_substract(self, _ignored):
        """
        When the subtract button is released
        :param _ignored: Unused parameter
        :return: None
        """
        self.event.set()
        if self.holding:
            self.holding = False
        else:
            self.subtract_button_callback()

    def on_release_add(self, _ignored):
        """
        When the add button is released
        :param _ignored: Unused parameter
        :return: None
        """
        self.event.set()
        if self.holding:
            self.holding = False
        else:
            self.add_button_callback()

    def mouse_hold(self, event, callback):
        """
        When the mouse is held on one of the buttons
        :param event: Event to wait for that represents the mouse release
        :param callback: Function to call when the mouse is held
        :return: None
        """
        count = 0
        while count < 3:
            time.sleep(.1)
            count += 1
            if event.is_set():
                return
        for i in range(5):
            self.holding = True
            callback()
            count = 0
            while count < 2:
                time.sleep(.1)
                count += 1
                if event.is_set():
                    return
        while True:

            callback()
            time.sleep(.1)
            if event.is_set():
                return
