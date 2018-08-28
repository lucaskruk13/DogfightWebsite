from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.models import User
from accounts.models import Profile, Scores
from feed.models import Course, Dogfight
from django.utils import timezone

# TODO: Create Currnet Player Table, Include Watiting List

class FeedView(TemplateView):
    template_name = 'feed/feed.html'



    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)



        # Add in a QuerySet of all the Courses
        context['course_list'] = Course.objects.all()
        context['dogfight'] = get_current_dogfight()
        context['scores_list'] = get_scores_list()


        return context





class CourseView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'feed/course.html'


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