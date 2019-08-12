import json

from django.test import TestCase, Client
from django.urls import reverse

from seating_planner_app.models import *


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.venues_url = reverse("venues")
        self.allocations_url = reverse("allocations")
        self.section = Section.create("test", [])
        self.section.save()
        self.allocation = Allocation(name="test", section=self.section, allocation=json.dumps(["test"]))
        self.allocation.save()

    def test_venues_GET(self):
        response = self.client.get(self.venues_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "venues-display.html")

    def test_get_allocations_POST(self):
        response = self.client.post(self.allocations_url, {
            "selection": self.section.name,
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "seat-allocations.html")
        self.assertEquals(response.context["allocations"][0]["allocation"], json.loads(self.allocation.allocation))

    def test_get_allocations_empty_POST(self):
        response = self.client.post(self.allocations_url, {
            "selection": "",
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "seat-allocations.html")
        self.assertEquals(response.context["allocations"], [])
