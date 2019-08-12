from django.test import SimpleTestCase
from django.urls import reverse, resolve

from seating_planner_app.views import get_allocations, display_venues


class TestUrls(SimpleTestCase):

    def test_venues_url_is_resolved(self):
        url = reverse("venues")
        self.assertEquals(resolve(url).func, display_venues)

    def test_allocations_url_is_resolved(self):
        url = reverse("allocations")
        self.assertEquals(resolve(url).func, get_allocations)
