from enum import Enum

import customtkinter


class StickerGenProgressBar(customtkinter.CTkProgressBar):
    class StickerProgressBarStates(float, Enum):
        STARTING = 0.1,
        GENERATING_IMG = 0.2,
        GENERATING_PDF = 0.6,
        DELETING_IMG = 0.8,
        DONE = 1

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.set(self.StickerProgressBarStates.STARTING.value)
        self.update()

    def set_state(self, state):
        self.set(state.value)
        self.update()

    def destroy(self):
        super().destroy()
