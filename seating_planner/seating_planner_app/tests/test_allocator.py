import seating_planner_app.allocator as allocator
from django.test import TestCase


class TestAllocator(TestCase):

    def test_get_next_row_even(self):
        initial_row = 0
        next_row = 1
        row_2 = ["row21", "row22"]
        row, updated_row = allocator.get_next_row(initial_row, [["row1"], row_2])
        self.assertEquals(row, list(reversed(row_2)))
        self.assertEquals(updated_row, next_row)

    def test_get_next_row_odd(self):
        initial_row = 1
        next_row = 2
        row_3 = ["row31", "row32"]
        row, updated_row = allocator.get_next_row(initial_row, [["row1"], ["row_2"], row_3])
        self.assertEquals(row, row_3)
        self.assertEquals(updated_row, next_row)

    def test_get_perfect_fit_pair(self):
        groups = [(0, 4), (1, 66), (2, 1), (3, 2)]
        results = allocator.get_perfect_fit(groups, 3)
        self.assertEquals(results[0], 2)
        self.assertEquals(results[1], 3)

    def test_get_perfect_fit_single(self):
        groups = [(0, 4), (1, 66), (2, 1), (3, 2)]
        results = allocator.get_perfect_fit(groups, 66)
        self.assertEquals(results[0], 1)
