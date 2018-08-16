from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User
from accounts.models import Profile, Scores

# Create your views here.
class FeedView(TemplateView):
    template_name = 'feed/feed.html'

