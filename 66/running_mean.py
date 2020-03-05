import itertools


def running_mean_old(sequence):
    """Calculate the running mean of the sequence passed in,
       returns a sequence of same length with the averages.
       You can assume all items in sequence are numeric."""
    sum_ = 0
    for idx, number in enumerate(sequence, start=1):
        sum_ += number
        yield round(sum_ / idx, 2)


def running_mean(sequence):
    for idx, total in enumerate(itertools.accumulate(sequence), start=1):
        yield round(total / idx, 2)
