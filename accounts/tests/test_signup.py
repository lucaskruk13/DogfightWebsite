from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your tests here.
class SignupTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('signup'))

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

class SuccessfulSignupUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username':'john',
            'email':'john@appleseed.com',
            'first_name':'john',
            'last_name':'appleseed',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
        }

        self.response = self.client.post(url, data)
        print (self.response)
        self.my_account_url = reverse('my_account')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the feed page
        '''

        self.assertRedirects(self.response, self.my_account_url)

    def test_user_creation(self):

        self.assertTrue(User.objects.exists())

    def test_user_authenticaion(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a 'user' to it's context, after a successful signup
        '''



        response = self.client.get(self.my_account_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())