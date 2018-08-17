from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.forms import ProfileForm

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


        data2 = {
            'bio': 'Its Me!',
            'handicap': 5,
        }

        self.response = self.client.post(url, data)
        self.my_account_url = reverse('my_account')

        self.account_response = self.client.get(self.my_account_url)

        self.response2_url = self.client.post(self.my_account_url, data2)
        self.feed_response = self.client.get(reverse('feed'))



    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the feed page
        '''

        self.assertRedirects(self.response, self.my_account_url)

    def test_user_creation(self):

        self.assertTrue(User.objects.exists())
        user = User.objects.first()


        self.assertTrue(Profile.objects.exists()) # Profile should be created



    def test_user_authenticaion(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a 'user' to it's context, after a successful signup
        '''

        response = self.client.get(self.my_account_url)
        self.user = response.context.get('user')
        self.assertTrue(self.user.is_authenticated)

    def test_profile_signup(self):
        user = self.feed_response.context.get('user')

        self.assertEquals('Its Me!', user.profile.bio)
        self.assertEquals(5.0, float(user.profile.handicap))

class ProfileCreation(TestCase):
    def setUp(self):
        url = reverse('signup')

        data = {
            'username': 'john',
            'email': 'john@appleseed.com',
            'first_name': 'john',
            'last_name': 'appleseed',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',

        }


        self.response = self.client.post(url, data)


    def test_profile_initial_value(self):
        # A profile should exist
        self.assertTrue(Profile.objects.exists())

        # The Profile should have a Initial Value, with a zero handicap
        profile = Profile.objects.first()
        self.assertTrue(profile.initial)
        self.assertEquals(float(profile.handicap), 0)

    def test_profile_update(self):
        account_url = reverse('my_account')

        data = {
            'handicap': 1.4,
            'bio': 'Its Me!',
        }

        proile_response = self.client.post(account_url, data)

        profile = Profile.objects.first() # Should be updated

        self.assertEquals(1.4, float(profile.handicap)) # ensure profile handicap is updated
        self.assertRedirects(proile_response, reverse('feed')) # Should redirect to Feed

# TODO: test invalid haidicap setup, example - Superuser doesnt initially have a handicap

# TODO: test quota is successfully created

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

class InvalidProfileSignup(TestCase):

    def setUp(self):
        url = reverse('signup')

        data = {
            'username': 'john',
            'email': 'john@appleseed.com',
            'first_name': 'john',
            'last_name': 'appleseed',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',

        }

        self.response = self.client.post(url, data)


        data = {
            'handicap': '2..5',
            'bio': 'its me',
        }

        # post an invalid form
        self.account_post = self.client.post(reverse('my_account'), data)
        self.account_response = self.client.get(reverse('my_account'))


    def test_account_status_code(self):

        self.assertEquals(self.account_post.status_code, 200)


    def test_csrf(self):
        self.assertContains(self.account_response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.account_response.context.get('form')
        self.assertIsInstance(form, ProfileForm)

    def test_form_errors_invalid_handicap(self):
        form = self.account_post.context.get('form')
        self.assertTrue(form.errors)
