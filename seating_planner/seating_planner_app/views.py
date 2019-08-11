from django.shortcuts import render
from seating_planner_app.models import *
from django.db.models import Count
import json


def get_allocations(request):
    sections = Section.objects.filter(name=request.POST["selection"])
    if len(sections) > 0:
        sect = sections[0]
        allocations = list(Allocation.objects.all().filter(section=sect))
        final_alls = []
        for a in allocations:
            a.allocation = json.loads(a.allocation)
            final_alls.append(vars(a))
        response = {"allocations": final_alls}
    else:
        response = {"allocations": []}
    return render(request, "seat-allocations.html", response)


def display_venues(request):
    response = {"venues": Section.objects.all().annotate(seats_num=Count("allocation"))}
    return render(request, "venues-display.html", response)
