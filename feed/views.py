from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.models import User
from accounts.models import Profile, Scores
from feed.models import Course, Dogfight
from django.utils import timezone
from feed.forms import DogfightSignupForm
from django.contrib import messages

# TODO: Create Currnet Player Table, Include Watiting List

class FeedView(TemplateView):
    template_name = 'feed/feed.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        dogfight = get_current_dogfight()

        # Add in a QuerySet of all the Courses
        context['course_list'] = Course.objects.all()
        context['dogfight'] = dogfight
        context['scores_list'] = get_scores_list()
        context['signed_up'] = is_signed_up(self.request.user, dogfight)

        return context


class CourseView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'feed/course.html'


# Creating a url to sign up the golfer
# TODO: Write Dogfight Signup Tests. Nothing started as of yet.
def dogfight_signup(request, dogfight_pk, user_pk):

    user = request.user # Get the requesting User
    dogfight = get_current_dogfight() # Get the Current User

    score = Scores.objects.create(user=user, dogfight=dogfight) # Create the Score Object, Thus, singing them up

    if score:
        messages.success(request, 'Sign Up Successful!')

    return redirect('feed') # Redirect to the Feed becuase we have nothing else to show them.

# TODO: Write Cancel Dogfight Tests.
def cancel_dogfight_signup(request, dogfight_pk, user_pk):

    user = request.user
    dogfight = get_current_dogfight()

    score = Scores.objects.filter(user=user, dogfight=dogfight).delete()

    return redirect('feed')

def is_signed_up(user, dogfight):
    # Get All The user Scores

    if not user.is_anonymous and dogfight:

        # check to see if this dogfight is in the user scores. If the count is greater than 0 then we know they are signed up
        if Scores.objects.filter(user=user, dogfight=dogfight).count():
            return True

    return False



def get_scores_list():
    dogfight = get_current_dogfight()
    return Scores.objects.filter(dogfight=dogfight).order_by('user__last_name')


def get_current_dogfight():

    dogfight = Dogfight.objects.filter(date__gte=timezone.now()).order_by('date').first() # Gets the upcoming dogfight, even if there are dogfights scheduled for a later date
    return dogfight


# Yield successive n-sized
# chunks from l.
def create_groups(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]