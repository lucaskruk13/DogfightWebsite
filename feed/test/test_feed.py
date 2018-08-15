from django.test import TestCase
from django.urls import reverse, resolve
from feed.views import FeedView

# Create your tests here.

class FeedTests(TestCase):

    def setUp(self):
        self.url = reverse('feed')
        self.response = self.client.get(self.url)

    def test_feed_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_feed_url_resolves_feed_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, FeedView)