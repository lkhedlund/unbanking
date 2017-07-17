from django import forms
from django.core.exceptions import ValidationError

from .models import Submission, Vote
from .utils import contains_profanity

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['word', ]
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': 'Submit or vote for a word!'}),
        }

    def clean_word(self):
        word = self.cleaned_data['word']
        if contains_profanity(word):
            raise ValidationError("Let's keep it classy. Please suggest another word.")
        else:
            return word

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['submission', ]
