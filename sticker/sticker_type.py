from datetime import datetime

from sticker.sticker_data import StickerDataNumber, StickerDataText, StickerDataDate, StickerDataList
from sticker.sticker_generation import StickerGenerator


class StickerType:
    """
    Class to represent a sticker
    """
    def __init__(self, name, data, align="left"):
        """
        StickerType constructor
        :param name: Name of the sticker
        :param data: List of StickerData
        :param align: Alignment of the sticker when printed
        :return: None
        """
        self.name = name
        self.align = align
        self.data = data

    def __str__(self):
        """
        String representation of the sticker
        :return: The name of the sticker
        """
        return self.name

    def is_valid(self):
        """
        Check if it is a valid sticker
        :return: False if one of the data is not valid, True otherwise
        """
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
        """
        Convert a date to the format dd/mm/yyyy
        :param date: Date to convert
        :return: The date in the format dd/mm/yyyy
        :raises Exception: If the date is not in a valid format
        """
        for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y'):
            try:
                date = datetime.strptime(date, fmt)
                return date.strftime('%d/%m/%Y')
            except ValueError:
                pass
        raise Exception('no valid date format found')

    def generate(self, save_file_path, state_callback=None, **kwargs):
        """
        Generate the sticker
        :param save_file_path: Path to save the sticker
        :param state_callback: Callback function for updating progress bar states corresponding to the current state
        :param kwargs: Keyword arguments for the pdf generation (stickers_left, total_stickers)
        :return: None
        """
        sticker_generator = StickerGenerator(state_callback)
        sticker_generator.generate_stickers(self, save_file_path, **kwargs)
