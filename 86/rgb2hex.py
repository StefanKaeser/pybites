def rgb_to_hex(rgb):
    """Receives (r, g, b)  tuple, checks if each rgb int is within RGB
       boundaries (0, 255) and returns its converted hex, for example:
       Silver: input tuple = (192,192,192) -> output hex str = #C0C0C0"""
    if not all(0 <= color_value <= 255 for color_value in rgb):
        raise ValueError(f"The input {rgb} is not valid RGB code.")

    hex_string = "".join("%02x" % color_value for color_value in rgb)
    hex_string = "#" + hex_string.upper()

    return hex_string
