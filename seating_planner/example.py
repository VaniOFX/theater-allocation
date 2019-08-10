from enum import Enum, auto

class Rank(Enum):
    RANK_1 = auto()
    RANK_2 = auto()
    RANK_3 = auto()

class Extra(Enum):
    AISLE = auto()
    FRONT_ROW = auto()
    HIGH = auto()
    NONE = auto()

class Seat():
    def __init__(self, rank:Rank, blocked=False, extra=Extra.NONE):
        self.rank = rank
        self.extra = extra
        self.blocked = blocked
        self.taken_by = 0

    def __repr__(self):
        return f"{self.taken_by}"

class Section():
    def __init__(self, name, rows):
        self.rows = rows
        self.layout = rows.copy()
        self.name = name
        self.__next_empty = 0

    def allocate_groups(self, rank, groups):
        curr_seat_id = 0
        curr_row = self.get_next_row()
        group_tups = [(i, group_size) for i, group_size in enumerate(groups)]
        group_tups_urgent = []
        looping_indicator = False

        while len(group_tups) > 0 or len(group_tups_urgent) > 0:
            if (len(group_tups_urgent) == 0 or looping_indicator) and len(group_tups) > 0:
                curr_group_num, curr_group_size = group_tups.pop(0)
            else:
                curr_group_num, curr_group_size = group_tups_urgent.pop(0)

            remaining_seats = self.get_remaining_seats(curr_seat_id, curr_row)

            if remaining_seats > 0 and remaining_seats - curr_group_size <= -1 and len(group_tups) > 0:
                looping_indicator = True
                idx = self.get_perfect_fit(group_tups, remaining_seats)
                if idx[0] != -1:
                    for i in idx:
                        group_tups_urgent.insert(0, group_tups.pop(i))
                        looping_indicator = False
                group_tups_urgent.append((curr_group_num, curr_group_size))
                continue

            for _ in range(curr_group_size):
                # if the row is full continue to the next one
                if self.get_remaining_seats(curr_seat_id, curr_row) <= 0:
                    curr_row = self.get_next_row()
                    curr_seat_id = 0

                # allocate the next seat
                curr_seat = curr_row[curr_seat_id]
                if curr_seat.rank == rank:
                    curr_seat.taken_by = curr_group_num
                curr_seat_id += 1
                looping_indicator = False

    def get_remaining_seats(self, current_seat_index, current_row):
        return len(current_row) - current_seat_index

    def get_perfect_fit(self, groups, seats_left):
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

        if perf_fit_idx[0] > 0 and idxs[0] > 0:
            return perf_fit_idx if perf_fit_idx[0] < idxs[0] else idxs
        else:
            return perf_fit_idx if perf_fit_idx[0] > idxs[0] else idxs


    def get_next_row(self):
        #change the direction of the allocation -> and <-
        direction = 1 if self.__next_empty % 2 == 0 else -1
        row = self.rows[self.__next_empty][::direction]
        self.__next_empty += 1
        return row


class Venue():
    def __init__(self, name, sections):
        self.name = name
        self.sections = sections

    def allocate_groups(self, rank, groups):
        for section in self.sections:
            section.allocate_groups(rank, groups)

    def save(self):



groups = [1, 3, 5, 4, 5, 4, 4, 6]

venue = Venue("concert",[
    Section("main",[
        [Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1)],
        [Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1)],
        [Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1)],
        [Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1), Seat(Rank.RANK_1)]
    ])
])

venue.allocate_groups(Rank.RANK_1, groups)
for row in venue.sections[0].rows:
    print(row)