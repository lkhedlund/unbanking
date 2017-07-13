from django.shortcuts import render
from django.views import generic
from django.db.models import Count

from .models import Submission, Vote

class IndexView(generic.ListView):
    template_name = 'upvote/index.html'
    context_object_name = 'top_submissions'

    def get_queryset(self):
        return Submission.objects \
            .annotate(votes=Count('vote')) \
            .order_by('-votes')[:20]