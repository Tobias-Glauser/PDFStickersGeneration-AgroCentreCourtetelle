import json
import os
import locale

from UI.gui import App
from sticker.stickers import Stickers
from sticker.sticker_data import StickerDataNumber, StickerDataText, StickerDataDate, StickerDataList
from sticker.sticker_type import StickerType


def empty_tmp():
    """
    Empty the tmp folder
    :return: None
    """
    for file in os.scandir(os.getcwd() + "\\tmp"):
        os.remove(file.path)


def set_locale():
    """
    Set the locale time to the system's locale time
    :return: None
    """
    locale.setlocale(locale.LC_TIME, '')


def get_stickers():
    """
    Get the stickers from the data.json file and create the Stickers object
    :return: The Stickers object
    """
    data = json.load(open('model/data.json', encoding='utf-8-sig'))

    stickers = Stickers()
    for sticker in data:
        datas = []
        for data in sticker['data']:
            if data['type'] == 'number':
                datas.append(StickerDataNumber(data['name'],
                                               inlineprefix=data['inline_prefix'],
                                               inlinesuffix=data['inline_suffix'],
                                               blockprefix=data['block_prefix'],
                                               blocksuffix=data['block_suffix'],
                                               font=data['font'],
                                               prefixfont=data['prefix_font'],
                                               suffixfont=data['suffix_font']))
            elif data['type'] == 'text':
                datas.append(StickerDataText(data['name'],
                                             inlineprefix=data['inline_prefix'],
                                             inlinesuffix=data['inline_suffix'],
                                             blockprefix=data['block_prefix'],
                                             blocksuffix=data['block_suffix'],
                                             font=data['font'],
                                             prefixfont=data['prefix_font'],
                                             suffixfont=data['suffix_font']))
            elif data['type'] == 'date':
                datas.append(StickerDataDate(data['name'],
                                             inlineprefix=data['inline_prefix'],
                                             inlinesuffix=data['inline_suffix'],
                                             blockprefix=data['block_prefix'],
                                             blocksuffix=data['block_suffix'],
                                             font=data['font'],
                                             prefixfont=data['prefix_font'],
                                             suffixfont=data['suffix_font']))
            elif data['type'] == 'list':
                datas.append(StickerDataList(data['name'],
                                             data['values'],
                                             inlineprefix=data['inline_prefix'],
                                             inlinesuffix=data['inline_suffix'],
                                             blockprefix=data['block_prefix'],
                                             blocksuffix=data['block_suffix'],
                                             font=data['font'],
                                             prefixfont=data['prefix_font'],
                                             suffixfont=data['suffix_font']))

        stickers.add_sticker(StickerType(sticker['name'], datas, align=sticker['align']))

    return stickers


def main():
    """
    Main function
    :return: None
    """
    set_locale()
    empty_tmp()
    stickers = get_stickers()
    app = App(stickers)
    app.mainloop()


if __name__ == "__main__":
    main()
