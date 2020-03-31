import re


def get_sentences(text):
    """Return a list of sentences as extracted from the text passed in.
       A sentence starts with [A-Z] and ends with [.?!]"""
    sentence_regex = re.compile(r"([A-Z].*?[.?!])(?= [A-Z]|$)", re.DOTALL)
    sentences = sentence_regex.findall(text.strip().replace("\n", " "))
    return sentences
