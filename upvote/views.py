from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Submission, Vote
from .forms import SubmissionForm

class IndexView(generic.View):
    template_name = 'upvote/index.html'
    paginate_by = 10

    def get(self, request):
        submission_form = SubmissionForm()
        submissions = Submission.objects \
            .annotate(votes=Count('vote')) \
            .order_by('-votes')
        page = request.GET.get('page', 1)
        paginator = Paginator(submissions, self.paginate_by)
        try:
            top_submissions = paginator.page(page)
        except PageNotAnInteger:
            top_submissions = paginator.page(1)
        except EmptyPage:
            top_submissions = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            'submission_form': submission_form,
            'top_submissions': top_submissions,
            })

    def post(self, request):
        form = SubmissionForm(request.POST)
        submitted_word = form.data['word'].lower()
        if Submission.objects.filter(word=submitted_word).exists():
            submission = Submission.objects.filter(word=submitted_word).get()
            vote = Vote(submission=submission)
            vote.save()
            messages.add_message(request, messages.INFO, "Already exists!")
            return HttpResponseRedirect(reverse('upvote:detail', args=(submission.word,)))
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

def vote(request, word):
    submission = get_object_or_404(Submission, word=word)
    vote = Vote(submission=submission)
    vote.save()
    return redirect('upvote:index')