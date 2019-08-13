def create_allocation(seats_layout, rank, groups):
    allocation = get_empty_allocation(seats_layout)

    # init variables
    curr_seat_id, curr_row_id = 0, 0
    curr_row = seats_layout[curr_row_id]
    group_tups = [(i, group_size) for i, group_size in enumerate(groups)]
    group_tups_urgent = []
    looping_indicator = False  # to prevent only getting urgent ones

    while len(group_tups) > 0 or len(group_tups_urgent) > 0:

        # decide which queue to get from, giving priority to the urgent ones
        if len(group_tups_urgent) == 0 and len(group_tups) > 0:
            curr_group_num, curr_group_size = group_tups.pop(0)
        else:
            curr_group_num, curr_group_size = group_tups_urgent.pop(0)

        # check if one person will be away from the group
        remaining_seats = get_remaining_seats_number(curr_seat_id, curr_row)
        alone_person = curr_group_size - remaining_seats == 1 or (remaining_seats == 1 and curr_group_size > 1)
        if alone_person and not looping_indicator:
            looping_indicator = True

            # check for a perfect fit and place them instead if available
            idx = get_perfect_fit(group_tups, remaining_seats)
            if idx[0] != -1:
                for i in idx:
                    group_tups_urgent.insert(0, group_tups.pop(i))
                    looping_indicator = False

            group_tups_urgent.append((curr_group_num, curr_group_size))
            continue

        for _ in range(curr_group_size):
            # if the row is full continue to the next one
            if get_remaining_seats_number(curr_seat_id, curr_row) <= 0:
                curr_row, curr_row_id = get_next_row(curr_row_id, seats_layout)
                curr_seat_id = 0

            # allocate the next seat
            curr_seat = curr_row[curr_seat_id]
            if curr_seat.rank == rank:
                allocation[curr_row_id][curr_seat_id] = curr_group_num + 1
            curr_seat_id += 1
            looping_indicator = False

    # reverse every other row of the allocation
    for i, row in enumerate(allocation):
        allocation[i] = row[::-1] if i % 2 != 0 else row

    return allocation


def get_empty_allocation(layout):
    allocation = []
    for row in layout:
        tmp_row = []
        for _ in row:
            tmp_row.append(-1)
        allocation.append(tmp_row)

    return allocation


def get_remaining_seats_number(current_seat_index, current_row):
    return len(current_row) - current_seat_index


def get_perfect_fit(groups, seats_left):
    groups_flat = [i[1] for i in groups]

    # get a  single perfect fit
    perf_fit_idx = [groups_flat.index(seats_left)] if seats_left in groups_flat else [-1]

    # get a perfect fit with 2 groups
    lookup = {}
    idxs = [-1, -1]
    for i, curr_group_size in enumerate(groups_flat):
        if seats_left - curr_group_size in lookup:
            idxs = [lookup[seats_left - curr_group_size], i]
            break
        lookup[curr_group_size] = i

    # decide which one to return (the one with higher priority - comes first in the list with group sizes)
    if perf_fit_idx[0] > 0 and idxs[0] > 0:
        return perf_fit_idx if perf_fit_idx[0] < idxs[0] else idxs
    else:
        return perf_fit_idx if perf_fit_idx[0] > idxs[0] else idxs


def get_next_row(current_row, layout):
    next_row = current_row + 1
    if next_row < len(layout):
        # change the direction of the allocation -> and <-
        direction = 1 if next_row % 2 == 0 else -1
        row = layout[next_row][::direction]
    else:
        row = []
    return row, next_row
