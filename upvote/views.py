from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Submission, Vote
from .forms import SubmissionForm
from .utils import has_voted, format_word

class IndexView(generic.View):
    template_name = 'upvote/index.html'
    paginate_by = 10

    duplicate_message = "Great minds think alike! Your word has already been chosen, so we've aded a vote. Don't tell anyone else, but we hope you win."
    thanks_message = "Thank you for your submission! Now get out there and vote!"

    def get(self, request):
        form = SubmissionForm()
        submissions = Submission.objects \
            .annotate(votes=Count('vote')) \
            .order_by('-votes') \
            .filter(disabled=False)
        page = request.GET.get('page', 1)
        paginator = Paginator(submissions, self.paginate_by)
        try:
            top_submissions = paginator.page(page)
        except PageNotAnInteger:
            top_submissions = paginator.page(1)
        except EmptyPage:
            top_submissions = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            'form': form,
            'top_submissions': top_submissions,
            })

    def post(self, request):
        form = SubmissionForm(request.POST)
        # Check whether the user has already submitted a word or voted
        submitted_word = format_word(form.data['word'])
        if Submission.objects.filter(word=submitted_word).exists():
            submission = Submission.objects.filter(word=submitted_word).get()
            if has_voted(request):
                return redirect('upvote:index')
            vote = Vote(submission=submission)
            vote.save()
            messages.add_message(request, messages.INFO, self.duplicate_message)
            request.session['has_voted'] = True
            return HttpResponseRedirect(reverse('upvote:detail', args=(submission.word,)))
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            messages.add_message(request, messages.INFO, self.thanks_message)
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
    if has_voted(request):
        return redirect('upvote:index')
    submission = get_object_or_404(Submission, word=word)
    vote = Vote(submission=submission)
    vote.save()
    request.session['has_voted'] = True
    return redirect('upvote:index')