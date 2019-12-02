import textwrap


INDENTS = 4


def print_hanging_indents(poem):
    seperater = "\n" + " " * INDENTS

    # Use dedent to get rid of leading whitespace on every line
    # Also break at double newline, i.e. new stanza
    for stanza in textwrap.dedent(poem[1:]).split("\n\n"):
        print(seperater.join(stanza.split("\n")))
