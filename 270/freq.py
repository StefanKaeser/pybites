from collections import Counter

def freq_digit(num: int) -> int:
    digit_occurences = Counter(str(num))
    most_frequent_digit = digit_occurences.most_common(1)[0][0]
    return int(most_frequent_digit)
