import os
import django
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seating_planner.settings')
django.setup()
from seating_planner_app.models import *
from seating_planner_app import allocator

if __name__ == "__main__":
    layout = [
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2), (Rank.RANK_1, 3), (Rank.RANK_1, 4), (Rank.RANK_1, 5), (Rank.RANK_1, 6),
         (Rank.RANK_1, 7), (Rank.RANK_1, 8)],
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2), (Rank.RANK_1, 3), (Rank.RANK_1, 4), (Rank.RANK_1, 5), (Rank.RANK_1, 6),
         (Rank.RANK_1, 7), (Rank.RANK_1, 8)],
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2), (Rank.RANK_1, 3), (Rank.RANK_1, 4), (Rank.RANK_1, 5), (Rank.RANK_1, 6),
         (Rank.RANK_1, 7), (Rank.RANK_1, 8)],
        [(Rank.RANK_1, 1), (Rank.RANK_1, 2), (Rank.RANK_1, 3), (Rank.RANK_1, 4), (Rank.RANK_1, 5), (Rank.RANK_1, 6),
         (Rank.RANK_1, 7), (Rank.RANK_1, 8)]
        ]

    # clean-up db (cascades all the Seat and Allocation objects too)
    Section.objects.all().delete()
    sect = Section.create("balcony", layout)
    sect.save()

    groups = [1, 2, 2, 3, 3, 4, 3, 6]
    allocation = allocator.create_allocation(sect.get_layout(), Rank.RANK_1, groups)
    Allocation(name="Championship", allocation=json.dumps(allocation), section=sect).save()

    allocation_json = Allocation.objects.get(section=sect).allocation
    allocation = json.loads(allocation_json)

    for row in allocation:
        print(row)
