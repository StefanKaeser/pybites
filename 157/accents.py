import unicodedata


def filter_accents(text):
    """Return a sequence of accented characters found in
       the passed in lowercased text string
    """
    accents = []
    for char in text:
        if "WITH" in unicodedata.name(char):
            accents.append(char.lower())
    return accents
