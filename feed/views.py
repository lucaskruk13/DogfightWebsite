from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView

# Create your views here.
class FeedView(TemplateView):
    template_name = 'feed/feed.html'