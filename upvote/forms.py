from django import forms
from .models import Submission, Vote

from .utils import validate_profanity

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['word', ]
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': 'Submit or vote for a word!'}),
        }

    def clean_word(self):
        word = self.cleaned_data['word']
        validate_profanity(word)
        return word

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['submission', ]
