COL_WIDTH = 20


def cut_words_from_line(line, width=COL_WIDTH):
    if len(line) <= width:
        return line + " " * (width - len(line)), ""
    cut = width
    while line[cut] != " ":
        cut -= 1
    return line[:cut] + " " * (width - cut), line[cut:].strip()


def cut_line_in_rows(line, width=COL_WIDTH):
    rows = []
    while line != "":
        row, line = cut_words_from_line(line, width=COL_WIDTH)
        rows.append(row)
    return rows


def text_to_columns(text):
    """Split text (input arg) to columns, the amount of double
       newlines (\n\n) in text determines the amount of columns.
       Return a string with the column output like:
       line1\nline2\nline3\n ... etc ...
       See also the tests for more info."""
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n")]
    rows = [cut_line_in_rows(paragraph) for paragraph in paragraphs]
    rows = ["\t".join(row) for row in zip(*rows)]
    return "\n".join(rows)
