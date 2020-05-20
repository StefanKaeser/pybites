IMPOSSIBLE = 'Mission impossible. No one can contribute.'


def max_fund(village):
    """Find a contiguous subarray with the largest sum."""
    # Hint: while iterating, you could save the best_sum collected so far
    # return total, starting, ending
    all_negative = all(villager < 0 for villager in village)
    if all_negative:
        print(IMPOSSIBLE)
        return (0, 0, 0)

    best_sum, best_start, best_stop = 0, 0, 0

    current_sum = 0
    for current_stop, value in enumerate(village):
        if current_sum <= 0:
            current_start = current_stop
            current_sum = value
        else:
            current_sum += value

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_stop = current_stop

    return (best_sum, best_start+1, best_stop+1)
