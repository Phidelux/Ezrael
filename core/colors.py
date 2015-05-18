import random


class Color:
    MAX_COLOR_IDX = 15

    colors = [
        '\x03' + '01', '\x03' + '02', '\x03' + '03', '\x03' + '04',
        '\x03' + '05', '\x03' + '06', '\x03' + '07', '\x03' + '08',
        '\x03' + '09', '\x03' + '10', '\x03' + '11', '\x03' + '12',
        '\x03' + '13', '\x03' + '14', '\x03' + '15', '\x03' + '16'
    ]

    black = '\x03' + '01'
    navy_blue = '\x03' + '02'
    green = '\x03' + '03'
    red = '\x03' + '04'
    brown = '\x03' + '05'
    purple = '\x03' + '06'
    olive = '\x03' + '07'
    yellow = '\x03' + '08'
    lime_green = '\x03' + '09'
    teal = '\x03' + '10'
    aqua_light = '\x03' + '11'
    royal_blue = '\x03' + '12'
    hot_pink = '\x03' + '13'
    dark_gray = '\x03' + '14'
    light_gray = '\x03' + '15'
    white = '\x03' + '16'

    bold = '\x02'
    italic = '\x09'
    underline = '\x15'
    clear = '\x0f'
    underline2 = '\x1f'
    reverse = '\x16'
    strike_through = '\x13'

    @staticmethod
    def random():
        return Color.colors[random.randint(0, Color.MAX_COLOR_IDX)]
