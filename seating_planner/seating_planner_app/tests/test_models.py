from django.test import TestCase

from seating_planner_app.models import Section, Seat, Rank


class TestModels(TestCase):

    def setUp(self):
        self.section = Section.create("test", [[(Rank.RANK_1, 1), (Rank.RANK_1, 2)]])
        self.section.save()

    def test_section_saving_seats(self):
        seats_count = 0
        for row in self.section.layout:
            for _ in row:
                seats_count += 1
        count = Seat.objects.count()
        self.assertEquals(count, seats_count)

    def test_get_section_layout(self):
        layout = self.section.layout
        self.assertEquals(layout[0][0].seat_num, 1)
        self.assertEquals(layout[0][1].seat_num, 2)
