def dec_to_base(number, base):
    """
    Input: number is the number to be converted
           base is the new base  (eg. 2, 6, or 8)
    Output: the converted number in the new base without the prefix (eg. '0b')
    """
    digits = []

    def factorize(number):
        if number < base:
            digits.append(number)
        else:
            rest = int(number % base)
            digits.append(rest)
            number = int(number / base)
            factorize(number)

    factorize(number)
    number_in_base = digits_to_number(digits)
    return number_in_base


def digits_to_number(digits):
    return int("".join([str(digit) for digit in digits[::-1]]))
