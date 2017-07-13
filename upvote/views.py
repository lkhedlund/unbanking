from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db.models import Count

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
            return redirect('upvotes:thanks')
        return redirect('upvotes:index')

def thanks(request):
    return render(request, 'upvote/thanks.html')