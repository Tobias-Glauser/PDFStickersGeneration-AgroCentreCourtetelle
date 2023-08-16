from abc import ABC


class StickerData(ABC):
    """
    Base class for sticker data (Abstract class)
    """
    def __init__(self, name,
                 value=None,
                 inlineprefix=None,
                 inlinesuffix=None,
                 blockprefix=None,
                 blocksuffix=None,
                 font='normal',
                 prefixfont=None,
                 suffixfont=None):
        """
        StickerData class constructor
        :param name: Name of the sticker data
        :param value: Value of the sticker data
        :param inlineprefix: Prefix to add inline before the value when printing the sticker
        :param inlinesuffix: Suffix to add inline after the value when printing the sticker
        :param blockprefix: Prefix to add in a block before the value when printing the sticker
        :param blocksuffix: Suffix to add in a block after the value when printing the sticker
        :param font: Font to use for the value when printing the sticker
        :param prefixfont: Font to use for the prefix when printing the sticker
        :param suffixfont: Font to use for the suffix when printing the sticker
        """
        self.name = name
        self.value = value
        self.inlineprefix = inlineprefix
        self.inlinesuffix = inlinesuffix
        self.blockprefix = blockprefix
        self.blocksuffix = blocksuffix
        self.font = font
        self.prefixfont = prefixfont or font
        self.suffixfont = suffixfont or font


class StickerDataNumber(StickerData):
    """
    Class for sticker data of type number
    """
    def __init__(self, name, **kwargs):
        """
        StickerDataNumber class constructor
        :param name: Name of the sticker data
        :param kwargs: Keyword arguments for the StickerData class constructor
        """
        super().__init__(name, **kwargs)


class StickerDataText(StickerData):
    """
    Class for sticker data of type text
    """
    def __init__(self, name, **kwargs):
        """
        StickerDataText class constructor
        :param name: Name of the sticker data
        :param kwargs: Keyword arguments for the StickerData class constructor
        """
        super().__init__(name, **kwargs)


class StickerDataDate(StickerData):
    """
    Class for sticker data of type date
    """
    def __init__(self, name, **kwargs):
        """
        StickerDataDate class constructor
        :param name: Name of the sticker data
        :param kwargs: Keyword arguments for the StickerData class constructor
        """
        super().__init__(name, **kwargs)


class StickerDataList(StickerData):
    """
    Class for sticker data of type list
    """
    def __init__(self, name, values, **kwargs):
        """
        StickerDataList class constructor
        :param name: Name of the sticker data
        :param values: Possible values for the sticker data
        :param kwargs: Keyword arguments for the StickerData class constructor
        """
        super().__init__(name, **kwargs)
        self.values = values
