from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Submission, Vote
from .forms import SubmissionForm

class IndexView(generic.View):
    template_name = 'upvote/index.html'

    def get(self, request):
        submission_form = SubmissionForm()
        submissions = Submission.objects \
            .annotate(votes=Count('vote')) \
            .order_by('-votes')[:20]
        return render(request, self.template_name, {
            'submission_form': submission_form,
            'top_submissions': submissions,
            })

    def post(self, request):
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            messages.add_message(request, messages.INFO, "Thank you for your submission!")
            return HttpResponseRedirect(reverse('upvote:detail', args=(submission.word,)))
        return redirect('upvote:index')

class DetailView(generic.View):
    model = Submission
    template_name = 'upvote/detail.html'

    def get(self, request, word):
        submission = get_object_or_404(Submission, word=word)
        return render(request, self.template_name, {
            'submission': submission,
        })

def thanks(request):
    return render(request, 'upvote/thanks.html')