from django.test import TestCase
from django.urls import reverse, resolve
from feed.views import FeedView, CourseView
from feed.models import Course

# Create your tests here.

class FeedTests(TestCase):
    fixtures = ['fixture_feed_course.json']

    def setUp(self):


        self.url = reverse('feed')
        self.response = self.client.get(self.url)


    def test_feed_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_feed_url_resolves_feed_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, FeedView)

    # Removed from homepage for now
    # def test_feed_has_courses(self):
    #     self.assertContains(self.response, 'class="card"', 3)


class CourseViewTests(TestCase):
    fixtures = ['fixture_feed_course.json']

    def setUp(self):
        self.course = Course.objects.first()

        self.url = reverse('course', kwargs={'pk': self.course.pk})
        self.response = self.client.get(self.url)

    def test_course_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_course_url_resolves_course_view(self):
        view = resolve('/course/1')
        self.assertEquals(view.func.view_class, CourseView)


