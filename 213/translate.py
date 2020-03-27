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
        originals = regex.findall(org_text)
        translations = regex.findall(trans_text)
        
        for translation, original in zip(translations, originals): 
            trans_text = trans_text.replace(translation, original)

    return trans_text
