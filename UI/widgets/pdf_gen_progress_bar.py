from enum import Enum

import customtkinter


class StickerGenProgressBar(customtkinter.CTkProgressBar):
    """
    Class to represent a progress bar for the sticker generation process
    """
    class StickerProgressBarStates(float, Enum):
        """
        Enum to represent the different states of the progress bar
        """
        STARTING = 0.1,
        GENERATING_IMG = 0.2,
        GENERATING_PDF = 0.6,
        DELETING_IMG = 0.8,
        DONE = 1

    def __init__(self, parent, **kwargs):
        """
        StickerGenProgressBar constructor
        :param parent: Parent frame
        :param kwargs: Keyword arguments for the customtkinter.CTkProgressBar class
        :return: None
        """
        super().__init__(parent, **kwargs)
        self.set(self.StickerProgressBarStates.STARTING.value)
        self.update()

    def set_state(self, state):
        """
        Set the state of the progress bar
        :param state: State to set the progress bar to
        :return: None
        """
        self.set(state.value)
        self.update()

    def destroy(self):
        """
        Destroy the progress bar
        :return: None
        """
        super().destroy()
