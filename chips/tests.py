from django.test import TestCase
from django.core.urlresolvers import reverse


class TestHome(TestCase):
    def test_page_health(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
