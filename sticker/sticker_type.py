from datetime import datetime

from sticker.sticker_data import StickerDataNumber, StickerDataText, StickerDataDate, StickerDataList
from sticker.sticker_generation import StickerGenerator


class StickerType:
    """This object represents a sticker."""

    def __init__(self, name, data, align="left"):
        self.name = name
        self.align = align
        self.data = data

    def __str__(self):
        return self.name

    def is_valid(self):
        for data in self.data:
            if isinstance(data, StickerDataText):
                if data.value is None or data.value == "":
                    return False
            elif isinstance(data, StickerDataNumber):
                if data.value is None or data.value == "":
                    return False
                try:
                    int(data.value)
                except ValueError:
                    return False
            elif isinstance(data, StickerDataDate):
                if data.value is None or data.value == "":
                    return False
                try:
                    data.value = StickerType.convert_date(data.value)
                except Exception as e:
                    print(e)
                    return False
            elif isinstance(data, StickerDataList):
                if data.value is None or data.value == "" or data.value not in data.values:
                    return False
        return True

    @staticmethod
    def convert_date(date):
        for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y'):
            try:
                date = datetime.strptime(date, fmt)
                return date.strftime('%d/%m/%Y')
            except ValueError:
                pass
        raise Exception('no valid date format found')

    def generate(self, save_file_path, state_callback=None, progress_bar_destroy_callback=None, **kwargs):
        try:
            sticker_generator = StickerGenerator(state_callback, progress_bar_destroy_callback)
            sticker_generator.generate_stickers(self, save_file_path, **kwargs)
        except Exception as e:
            if state_callback is not None:
                progress_bar_destroy_callback()
            raise e
