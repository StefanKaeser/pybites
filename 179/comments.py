import re


def strip_comments(code):
    single_line_comment = re.compile(r"\n((    )*(#.*))")
    inline_comment = re.compile(r"  # .*")
    multiline_comment = re.compile(r'(    )*""".*?"""\n?', re.DOTALL)

    regexs = [single_line_comment, inline_comment, multiline_comment]

    for regex in regexs:
        code = regex.sub("", code)

    return code
