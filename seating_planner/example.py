import os
import django
from django.core import management
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seating_planner.settings')
django.setup()
from seating_planner_app.models import *
from seating_planner_app import allocator

if __name__ == "__main__":
    layout = [

        # sequentially numbered seats
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2),
         (Rank.RANK_1, 3), (Rank.RANK_1, 4),
         (Rank.RANK_1, 5), (Rank.RANK_1, 6),
         (Rank.RANK_1, 7), (Rank.RANK_1, 8)],

        # non-sequentially numbered seats
        [(Rank.RANK_1, 1), (Rank.RANK_1, 11),
         (Rank.RANK_1, 3), (Rank.RANK_1, 33),
         (Rank.RANK_1, 5), (Rank.RANK_1, 55),
         (Rank.RANK_1, 7), (Rank.RANK_1, 77)],

        # sequentially numbered seats
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2),
         (Rank.RANK_1, 3), (Rank.RANK_1, 4),
         (Rank.RANK_1, 5), (Rank.RANK_1, 6),
         (Rank.RANK_1, 7), (Rank.RANK_1, 8)],

        # sequentially numbered seats
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2),
         (Rank.RANK_1, 3), (Rank.RANK_1, 4),
         (Rank.RANK_1, 5), (Rank.RANK_1, 6)],
    ]

    # clean-up db (cascades all the Seat and Allocation objects too)
    Section.objects.all().delete()
    sect = Section.create("balcony", layout)
    sect.save()

    groups = [
        [1, 3, 4, 4, 5, 1, 2, 4],
        [3, 3, 3, 2, 5, 5, 3, 6]
    ]

    for i, group in enumerate(groups):
        allocation = allocator.create_allocation(sect.layout, Rank.RANK_1, group)
        Allocation(name=f"Concert {i}", allocation=json.dumps(allocation), section=sect).save()

    management.call_command('test')
    management.call_command('runserver')
