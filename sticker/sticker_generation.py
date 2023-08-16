import os
import time

from datetime import datetime

from PIL import ImageFont, ImageDraw, Image as PILImage
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from UI.widgets.pdf_gen_progress_bar import StickerGenProgressBar


class StickerGenerator:
    """
    Class for generating stickers
    """
    fonts = {
        'normal': {
            'font': ImageFont.truetype("segoeui.ttf", 20),
            'real_size': None,
        },
        'bold': {
            'font': ImageFont.truetype("segoeuib.ttf", 20),
            'real_size': None,
        },
        'big': {
            'font': ImageFont.truetype("segoeui.ttf", 26),
            'real_size': None,
        },
        'big_bold': {
            'font': ImageFont.truetype("segoeuib.ttf", 26),
            'real_size': None,
        },
    }

    def __init__(self, state_callback=None):
        """
        StickerGenerator constructor
        :param state_callback: Callback function for updating progress bar states corresponding to the current state
        :return: None
        """
        self.state_callback = state_callback
        StickerGenerator.__generate_fonts_real_sizes()

    def generate_stickers(self, sticker, save_file_path, **kwargs):
        """
        Generates stickers in a pdf file
        :param sticker: Sticker to generate
        :param save_file_path: Path to which the pdf will be saved
        :param kwargs: Keyword arguments the pdf generation (stickers_left, total_stickers)
        :return: None
        """
        time.sleep(1.5)
        self.update_state_if_needed(StickerGenProgressBar.StickerProgressBarStates.GENERATING_IMG)
        sticker_img_path = StickerGenerator.create_sticker(sticker)

        self.state_callback(StickerGenProgressBar.StickerProgressBarStates.GENERATING_PDF)
        self.generate_pdf(save_file_path, sticker_img_path, **kwargs)

    def generate_pdf(self, save_file_path, sticker_img_path, stickers_left=24, total_stickers=24):
        """
        Creates a pdf file with a sticker image
        :param save_file_path: path to which the pdf will be saved
        :param sticker_img_path: path to the sticker image
        :param stickers_left: Number of stickers left on the page | default: 24 (full page)
        :param total_stickers: Number of stickers to print | default: 24 (full page)
        :return: None
        """
        if total_stickers is None:
            total_stickers = 24

        if stickers_left is None or stickers_left == 0 or stickers_left > 24:
            stickers_left = 24
        elif 6 > stickers_left > 0:
            raise Exception('Not enough stickers left to print the page')

        file_existed = os.path.exists(save_file_path)
        now = datetime.now()

        doc = SimpleDocTemplate(save_file_path, pagesize=A4, topMargin=-.2 * cm, bottomMargin=-.6 * cm,
                                leftMargin=0 * cm, rightMargin=0)
        flowables = []
        img = Image(sticker_img_path, width=6.5 * cm, height=3.4 * cm)

        tblstyle = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 7), colors.white),
            ('LEFTPADDING', (0, 0), (-1, 7), .2 * cm),
            ('RIGHTPADDING', (0, 0), (-1, 7), .2 * cm),
            ('TOPPADDING', (0, 0), (-1, 7), 0),
            ('BOTTOMPADDING', (0, 0), (-1, 7), 0),
        ])
        table_template = [
            [19, 20, 21],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
            [13, 14, 15],
            [16, 17, 18],
            [22, 23, 24],
        ]

        while total_stickers > 0:
            start_number = 24 - stickers_left + 1
            data = table_template.copy()

            for i in range(start_number,
                           start_number + total_stickers if total_stickers < 24 - start_number + 1 else 25):
                data = [[_el if _el != i else img for _el in _ar] for _ar in data]
                total_stickers -= 1

            data = [["" if not isinstance(_el, Image) else img for _el in _ar] for _ar in data]
            tbl = Table(data, colWidths=7 * cm, rowHeights=3.71 * cm)
            tbl.setStyle(tblstyle)
            flowables.append(tbl)

            stickers_left = 24

        doc.build(flowables)

        timeout = 0
        while not ((os.path.exists(save_file_path) or file_existed) and now.timestamp() < os.path.getmtime(
                save_file_path)):
            time.sleep(0.1)
            print("Waiting for pdf generation...")
            timeout += 1
            if timeout > 300:
                raise Exception("Timeout while waiting for pdf generation")

        self.update_state_if_needed(StickerGenProgressBar.StickerProgressBarStates.DELETING_IMG)
        time.sleep(1)
        os.remove(sticker_img_path)
        self.update_state_if_needed(StickerGenProgressBar.StickerProgressBarStates.DONE)
        time.sleep(0.5)

    def update_state_if_needed(self, state):
        """
        Updates the progress bar state if a callback function was provided
        :param state: State to which the progress bar will be updated
        :return: None
        """
        if self.state_callback is not None:
            self.state_callback(state)

    @staticmethod
    def create_sticker(sticker):
        """
        Creates a sticker image
        :param sticker: Sticker to generate
        :return: Path to the generated sticker image
        """
        img = PILImage.open(os.getcwd() + "\\sticker_img\\agrocentre_logo.png")
        draw = ImageDraw.Draw(img)

        text_y_coordinates = 0
        width = 301 - 84
        for data in sticker.data:

            prefix_line_offset, main_line_offset, suffix_line_offset = StickerGenerator.get_lines_offsets(sticker,
                                                                                                          data,
                                                                                                          width)

            if data.blockprefix:
                StickerGenerator.draw_element(data, draw, prefix_line_offset, text_y_coordinates, "blockprefix")
                text_y_coordinates += StickerGenerator.fonts[data.prefixfont]['real_size']

            if data.inlineprefix:
                StickerGenerator.draw_element(data, draw, main_line_offset, text_y_coordinates, "inlineprefix")
                main_line_offset += StickerGenerator.get_text_width(data.inlineprefix,
                                                                    StickerGenerator.fonts[data.prefixfont])

            StickerGenerator.draw_element(data, draw, main_line_offset, text_y_coordinates, "value")
            main_line_offset += StickerGenerator.get_text_width(data.value, StickerGenerator.fonts[data.font])

            if data.inlinesuffix:
                StickerGenerator.draw_element(data, draw, main_line_offset, text_y_coordinates, "inlinesuffix")
                main_line_offset += StickerGenerator.get_text_width(data.inlinesuffix,
                                                                    StickerGenerator.fonts[data.suffixfont])

            biggest_font = StickerGenerator.fonts[data.font]['real_size']
            if StickerGenerator.fonts[data.prefixfont]['real_size'] > biggest_font:
                biggest_font = StickerGenerator.fonts[data.prefixfont]['real_size']
            elif StickerGenerator.fonts[data.suffixfont]['real_size'] > biggest_font:
                biggest_font = StickerGenerator.fonts[data.suffixfont]['real_size']

            text_y_coordinates += biggest_font

            if data.blocksuffix:
                StickerGenerator.draw_element(data, draw, suffix_line_offset, text_y_coordinates, "blocksuffix")
                text_y_coordinates += StickerGenerator.fonts[data.suffixfont]['real_size']

            text_y_coordinates += 10

        sticker_path = os.path.join(os.getcwd(), "tmp", "sticker.png")
        img.save(sticker_path)

        return sticker_path

    @staticmethod
    def __generate_fonts_real_sizes():
        """
        Generates the real sizes of the fonts
        Only needs to be called once
        :return: None
        """
        if StickerGenerator.fonts['normal']['real_size'] is None:
            for key in StickerGenerator.fonts:
                ascent, descent = StickerGenerator.fonts[key]['font'].getmetrics()
                StickerGenerator.fonts[key]['real_size'] = \
                    StickerGenerator.fonts[key]['font'].getmask("AjQlafTB").getbbox()[3] - descent + 5

    @staticmethod
    def get_text_width(text, font_type):
        """
        Calculates the width of a text
        :param text: Text to calculate the width of
        :param font_type: Font type used to calculate the width
        :return: The width of the text
        """
        return font_type['font'].getmask(text.replace(" ", "_")).getbbox()[2]

    @staticmethod
    def get_line_size(data, elements):
        """
        Calculates the size of a line
        :param data: Data of the sticker to calculate the line size of
        :param elements: Elements from the data that are in the line
        :return: The total size of the line
        """
        total_size = 0
        for element in elements:
            if element not in ["blockprefix", "blocksuffix", "inlineprefix", "inlinesuffix", "value"]:
                raise Exception("Unknown element: " + element)

            elif element == "blockprefix" and len(data.blockprefix) > 0:
                total_size += StickerGenerator.get_text_width(data.blockprefix,
                                                              StickerGenerator.fonts[data.prefixfont])
            elif element == "blocksuffix" and len(data.blocksuffix) > 0:
                total_size += StickerGenerator.get_text_width(data.blocksuffix,
                                                              StickerGenerator.fonts[data.suffixfont])
            elif element == "inlineprefix" and len(data.inlineprefix) > 0:
                total_size += StickerGenerator.get_text_width(data.inlineprefix,
                                                              StickerGenerator.fonts[data.prefixfont])
            elif element == "inlinesuffix" and len(data.inlinesuffix) > 0:
                total_size += StickerGenerator.get_text_width(data.inlinesuffix,
                                                              StickerGenerator.fonts[data.suffixfont])
            elif element == "value" and len(data.value) > 0:
                total_size += StickerGenerator.get_text_width(data.value,
                                                              StickerGenerator.fonts[data.font])

        return total_size

    @staticmethod
    def element_to_big(size, max_size):
        """
        Checks if a line is too big for the sticker
        :param size: Size of the line
        :param max_size: Maximum size of the line
        :return: True if the line is too big, False otherwise
        """
        if size > max_size:
            return True
        return False

    @staticmethod
    def draw_element(data, draw, left_offset, text_y_coordinates, element_name):
        """
        Draws an element of the sticker on the sticker image
        :param data: Data of the sticker
        :param draw: ImageDraw object used to draw on the sticker image
        :param left_offset: Offset of the element on the left (x coordinate to start drawing at)
        :param text_y_coordinates: Y coordinate to start drawing at
        :param element_name: name of the element to draw of the sticker (present in the data (inlineprefix, value, ...)))
        :return: None
        """
        if element_name == "inlineprefix":
            StickerGenerator.draw_text(draw,
                                       left_offset,
                                       text_y_coordinates,
                                       data.inlineprefix,
                                       StickerGenerator.fonts[data.prefixfont]['font'])

        if element_name == "inlinesuffix":
            StickerGenerator.draw_text(draw,
                                       left_offset,
                                       text_y_coordinates,
                                       data.inlinesuffix,
                                       StickerGenerator.fonts[data.suffixfont]['font'])

        if element_name == "blockprefix":
            StickerGenerator.draw_text(draw,
                                       left_offset,
                                       text_y_coordinates,
                                       data.blockprefix,
                                       StickerGenerator.fonts[data.prefixfont]['font'])

        if element_name == "blocksuffix":
            StickerGenerator.draw_text(draw,
                                       left_offset,
                                       text_y_coordinates,
                                       data.blocksuffix,
                                       StickerGenerator.fonts[data.suffixfont]['font'])

        if element_name == "value":
            StickerGenerator.draw_text(draw,
                                       left_offset,
                                       text_y_coordinates,
                                       data.value,
                                       StickerGenerator.fonts[data.font]['font'])

    @staticmethod
    def draw_text(draw, left_offset, text_y_coordinates, text, font):
        """
        Draws text on the sticker image
        :param draw: ImageDraw object used to draw on the sticker image
        :param left_offset: Offset of the element on the left (x coordinate to start drawing at)
        :param text_y_coordinates: Y coordinate to start drawing at
        :param text: Text to draw
        :param font: Font to use to draw the text
        :return: None
        """
        draw.text((left_offset, text_y_coordinates),
                  text,
                  (0, 0, 0),
                  font=font)

    @staticmethod
    def get_lines_sizes(data, width):
        """
        Calculates the sizes of the lines of the sticker data
        :param data: Data of the sticker to calculate the line sizes of
        :param width: Maximum width of the sticker drawable area
        :return: prefix_line_size, main_line_size, suffix_line_size
        :raises Exception: If a line is too long
        """
        prefix_line_size = StickerGenerator.get_line_size(data, ["blockprefix"])
        main_line_size = StickerGenerator.get_line_size(data, ["inlineprefix", "value", "inlinesuffix"])
        suffix_line_size = StickerGenerator.get_line_size(data, ["blocksuffix"])

        if StickerGenerator.element_to_big(prefix_line_size, width):
            raise Exception("Line too long", data.name, data.blockprefix)
        if StickerGenerator.element_to_big(main_line_size, width):
            raise Exception("Line too long", data.name, data.inlinesuffix + data.value + data.inlinesuffix)
        if StickerGenerator.element_to_big(suffix_line_size, width):
            raise Exception("Line too long", data.name, data.blocksuffix)

        return prefix_line_size, main_line_size, suffix_line_size

    @staticmethod
    def get_lines_offsets(sticker, data, width):
        """
        Calculates the offsets of the lines of the sticker data
        :param sticker: sticker to calculate the line offsets of
        :param data: Data of the sticker to calculate the line offsets of
        :param width: Maximum width of the sticker drawable area
        :return: None
        """
        prefix_line_size, main_line_size, suffix_line_size = StickerGenerator.get_lines_sizes(data, width)

        prefix_line_offset = 84
        main_line_offset = 84
        suffix_line_offset = 84

        if sticker.align == 'center':
            prefix_line_offset += (width - prefix_line_size) / 2
            main_line_offset += (width - main_line_size) / 2
            suffix_line_offset += (width - suffix_line_size) / 2

        return prefix_line_offset, main_line_offset, suffix_line_offset
