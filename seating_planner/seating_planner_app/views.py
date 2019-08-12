from django.shortcuts import render
from seating_planner_app.models import *
from django.db.models import Count
import json


def get_allocations(request):
    section_name = request.POST.get("selection", "")
    if section_name != "":
        try:
            section = Section.objects.get(name=section_name)
            allocations = list(Allocation.objects.all().filter(section=section))
            final_alls = []
            for a in allocations:
                a.allocation = json.loads(a.allocation)
                final_alls.append(vars(a))
        except:
            final_alls = []
        response = {"allocations": final_alls}
    else:
        response = {"allocations": []}
    return render(request, "seat-allocations.html", response)


def display_venues(request):
    response = {"venues": Section.objects.all().annotate(seats_num=Count("allocation"))}
    return render(request, "venues-display.html", response)
