INDENTS = 4


def print_hanging_indents(poem):
    poem = poem.strip().split("\n")
    poem = [line.strip() for line in poem]

    emptyline_indices = [idx for idx, line in enumerate(poem) if not line]

    formatted_string = ""
    seperater = "\n" + " " * INDENTS
    for start, end in zip([-1] + emptyline_indices, emptyline_indices + [None]):
        formatted_string += seperater.join(poem[start + 1 : end]) + "\n"

    print(formatted_string[:-1])
