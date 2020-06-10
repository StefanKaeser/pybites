def binary_search(sequence, target):
    first_idx = 0
    last_idx = len(sequence) - 1

    while first_idx <= last_idx:
        middle_idx = get_middle_idx(first_idx, last_idx)
        middle_value = sequence[middle_idx]
        
        if middle_value == target:
            return middle_idx

        if target < middle_value:
            last_idx = middle_idx - 1
        elif target > middle_value:
            first_idx = middle_idx + 1

    return None


def get_middle_idx(first_idx, last_idx):
    middle_idx = first_idx + (last_idx - first_idx) // 2
    return middle_idx
