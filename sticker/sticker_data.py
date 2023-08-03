from abc import ABC


class StickerData(ABC):
    def __init__(self, name,
                 value=None,
                 inlineprefix=None,
                 inlinesuffix=None,
                 blockprefix=None,
                 blocksuffix=None,
                 font='normal',
                 prefixfont=None,
                 suffixfont=None):
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
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class StickerDataText(StickerData):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class StickerDataDate(StickerData):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class StickerDataList(StickerData):
    def __init__(self, name, values, **kwargs):
        super().__init__(name, **kwargs)
        self.values = values
