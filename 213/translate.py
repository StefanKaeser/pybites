import re


def fix_translation(org_text, trans_text):
    """Receives original English text as well as text returned by translator.
       Parse trans_text restoring the original (English) code (wrapped inside
       code and pre tags) into it. Return the fixed translation str
    """
    inline_code_re = re.compile(r"<code>(.*?)</code>")
    code_block_re = re.compile(r"<pre>(.*?)</pre>", re.DOTALL)

    regexs = [inline_code_re, code_block_re]

    for regex in regexs:
        originals = regex.finditer(org_text)
        trans_text = regex.sub(lambda _ : next(originals).group(), trans_text)

    return trans_text
