from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import signup

# Create your tests here.
class SignupTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('signup'))

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)