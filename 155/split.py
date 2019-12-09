def split_words_and_quoted_text(text):
    """Split string text by space unless it is
       wrapped inside double quotes, returning a list
       of the elements.

       For example
       if text =
       'Should give "3 elements only"'

       the resulting list would be:
       ['Should', 'give', '3 elements only']
    """
    text = text.split()

    formated_text = []
    while len(text) > 0:
        word = text.pop(0)

        if word[0] == '"':
            stay_together = [word[1:]]
            while True:
                word = text.pop(0)
                if word[-1] == '"':
                    stay_together.append(word[:-1])
                    break
                stay_together.append(word)
            formated_text.append(" ".join(stay_together))

        else:
            formated_text.append(word)

    return formated_text
