from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Submission, Vote
from .forms import SubmissionForm
from .utils import format_word


def index(request):
    template_name = 'upvote/index.html'
    paginate_by = 10

    duplicate_message = "Great minds think alike! Your word has already been submitted, so please choose another word or help vote this one to the top."
    thanks_message = "Thank you for your submission! Vote for your word to help it get to the top!"

    submissions = Submission.objects \
        .annotate(votes=Count('vote')) \
        .order_by('-votes') \
        .filter(disabled=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(submissions, paginate_by)
    try:
        top_submissions = paginator.page(page)
    except PageNotAnInteger:
        top_submissions = paginator.page(1)
    except EmptyPage:
        top_submissions = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        # Check whether the user has already submitted a word or voted
        submitted_word = format_word(form.data['word'])

        if Submission.objects.filter(word=submitted_word).exists():
            submission = Submission.objects.filter(word=submitted_word).get()
            messages.add_message(request, messages.INFO, duplicate_message)
            return HttpResponseRedirect(reverse('upvote:detail', args=(submission.slug,)))
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            messages.add_message(request, messages.SUCCESS, thanks_message)
            return HttpResponseRedirect(reverse('upvote:detail', args=(submission.slug,)))
    else:
        form = SubmissionForm()

    return render(request, template_name, {
        'form': form,
        'top_submissions': top_submissions,
        })

class DetailView(DetailView):
    model = Submission
    template_name = 'upvote/detail.html'

def vote(request, slug):
    submission = get_object_or_404(Submission, slug=slug)
    word = submission.word
    voted_list = request.session.get('voted', [])
    if word in voted_list:
        voted_message = "You've already voted for {word}, but you can always share to get more votes!".format(word=word.upper())
        messages.add_message(request, messages.WARNING, voted_message)
    else:
        vote = Vote(submission=submission)
        vote.save()
        voted_list.append(word)
        request.session['voted'] = voted_list
        messages.add_message(request, messages.SUCCESS, "Thank you for voting. Remember to share to help your word reach the top!")
    return redirect('upvote:index')

def ajax_vote(request):
    data = {}
    print(request.POST)
    if request.method == 'POST':
        slug = request.POST.get('slug')
        data['slug'] = slug
    data['error'] = "Error!"
    return JsonResponse(data)