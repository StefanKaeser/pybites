import textwrap
import itertools

COL_WIDTH = 20


def _pad(string, width=COL_WIDTH):
    length = len(string)
    if length > width:
        raise ValueError
    return string + " " * (width - length)


def _pad_list(lst, width=COL_WIDTH):
    return [_pad(line) for line in lst]


def text_to_columns(text):
    """Split text (input arg) to columns, the amount of double
       newlines (\n\n) in text determines the amount of columns.
       Return a string with the column output like:
       line1\nline2\nline3\n ... etc ...
       See also the tests for more info."""
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n")]
    rows = [textwrap.wrap(paragraph.strip(), COL_WIDTH) for paragraph in paragraphs]
    rows = [_pad_list(row) for row in rows]
    rows = [
        "\t".join(row)
        for row in itertools.zip_longest(*rows, fillvalue=" " * COL_WIDTH)
    ]
    return "\n".join(rows)
