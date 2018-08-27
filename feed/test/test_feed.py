from feed.views import FeedView, CourseView
from django.test import TestCase
from django.urls import reverse, resolve
from feed.models import Course, Dogfight, DogfightPlayer
from datetime import timezone
from django.utils import timezone
from django.contrib.auth.models import User


class FeedTest(TestCase):

    fixtures = ['course_fixture'] # Load Courses to every test case becuase it's non related data

    @classmethod
    def setUpClass(cls):
        super(FeedTest, cls).setUpClass()

        cls.url = reverse('feed')

    def setUp(self):
        self.feedResponse = self.client.get(self.url)
        self.feedView = resolve('/')

class TestDogfightNotSetup(FeedTest):


    @classmethod
    def setUpTestData(cls):
        # Create a dogfight with a date in the past. This will simulate no currnet dogfight availible.
        startdate = timezone.now() - timezone.timedelta(days=5)
        Dogfight.objects.create(date=startdate, course=Course.objects.first())

    def test_feed_status_code(self):
        self.assertTrue(Dogfight.objects.exists()) # Make Sure Dogfight Was Created
        self.assertEquals(self.feedResponse.status_code, 200)

    def test_feed_url_resolves_feed_view(self):
        self.assertEquals(self.feedView.func.view_class, FeedView)

    def test_no_dogfight_present(self):
        # If No Dogfight is present, then the parallax window will not show
        self.assertNotContains(self.feedResponse, 'class="parallax-window"')

class TestWithDogfightSetup(FeedTest):

    fixtures = ['initial_data', 'course_fixture']

    @classmethod
    def setUpTestData(cls):

        # Create a dogfight, defaulting logic should allow it to be picked up by the feed.
        dogfight = Dogfight.objects.create(course=Course.objects.first())
        DogfightPlayer.objects.create(user=User.objects.first(), dogfight=dogfight)


    def test_feed_status_code(self):
        self.assertEquals(self.feedResponse.status_code, 200)

        # Test Dogfight's exists
        dogfight = Dogfight.objects.first()
        dogfightPlayer = DogfightPlayer.objects.first()

        print (dogfight)
        print (dogfightPlayer)

    def test_dogfight_present(self):
        # If a dogfight is available, then the parallax window will show
        self.assertContains(self.feedResponse, 'class="parallax-window"')
        self.assertContains(self.feedResponse, 'feed-table') # referencing the Table ID



class TestNoSignups(FeedTest):

    def test_no_signup_table_present(self):
        self.assertNotContains(self.feedResponse, 'feed-table-container')


class TestMultipleDogfightsUpcoming(FeedTest):

    @classmethod
    def setUpTestData(cls):
        # Create a dogfight with a date in the past. This will simulate no currnet dogfight availible.

        startdate = timezone.now() + timezone.timedelta(days=2)
        extendedStartTime = timezone.now() + timezone.timedelta(days=8)
        farOffStartTime = timezone.now() + timezone.timedelta(days=15)


        Dogfight.objects.create(date=extendedStartTime, course=Course.objects.first()) # Next Weeks Dogfight
        Dogfight.objects.create(date=farOffStartTime, course=Course.objects.last()) # Week After
        Dogfight.objects.create(date=startdate, course=Course.objects.last())  # Upcoming in the future


    def test_the_upcoming_dogfight(self):
        currentDogfight = self.feedResponse.context.get('dogfight')
        self.assertTrue(currentDogfight.date, timezone.now() + timezone.timedelta(days=2))

        self.assertTrue(currentDogfight.course, Course.objects.first())