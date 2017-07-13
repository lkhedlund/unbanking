from django.shortcuts import render
from django.views import generic

from .models import Submission, Vote

class IndexView(generic.ListView):
    template_name = 'upvote/index.html'
    context_object_name = 'top_submissions'

    def get_queryset(self):
        return Submission.objects.all()[:20]