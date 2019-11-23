"""Color class

The following sites were consulted:
    http://www.99colors.net/
    https://www.webucator.com/blog/2015/03/python-color-constants-module/
"""
import os
import sys
import textwrap
import urllib.request

# PREWORK (don't modify): import colors, save to temp file and import
color_values_module = os.path.join('./', 'color_values.py')
urllib.request.urlretrieve('https://bit.ly/2MSuu4z',
                           color_values_module)

# should be importable now
from color_values import COLOR_NAMES  # noqa E402


class Color:
    """Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color):
        self.color = color
        self.rgb = COLOR_NAMES.get(color.upper())

    @classmethod
    def hex2rgb(cls, hex_str):
        """Class method that converts a hex value into an rgb one"""
        try:
            r, g, b = (int(ele, 16) for ele in textwrap.wrap(hex_str.lstrip("#"), 2))
        except ValueError:
            raise ValueError
        return r, g, b

    @classmethod
    def rgb2hex(cls, rgb):
        """Class method that converts an rgb value into a hex one"""
        if not len(rgb) == 3:
            raise ValueError
        if not all((type(ele) == int) and 0 <= ele <= 255 for ele in rgb):
            raise ValueError

        integer_to_hex = lambda x : hex(x)[2:] if len(hex(x)) == 4 else 2*hex(x)[2:] 
        return "#" + "".join(integer_to_hex(ele) for ele in rgb)

    def __repr__(self):
        """Returns the repl of the object"""
        return "%s(%r)"%(self.__class__.__name__, self.color)

    def __str__(self):
        """Returns the string value of the color object"""
        if not self.rgb:
            return "Unknown"
        return str(self.rgb)
