from django import forms
from .models import Submission, Vote

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['word', ]
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': 'Submit or vote for a word!'}),
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['submission', ]
