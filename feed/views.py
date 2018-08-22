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


        return context


class CourseView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'feed/course.html'



def get_current_dogfight():
    dogfight = Dogfight.objects.filter(date__gte=timezone.now()).order_by('date').first()
    return dogfight
