from django import forms
from django.core.exceptions import ValidationError

from .models import Submission, Vote
from .utils import contains_profanity

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['word', 'name']
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': 'Submit or find a word'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
        }

    def clean_word(self):
        word = self.cleaned_data['word']
        if contains_profanity(word):
            raise ValidationError("Let's keep it classy. Please suggest another word.")
        else:
            return word

    def clean_name(self):
        name = self.cleaned_data['name']
        print('In clean')
        if contains_profanity(name, False):
            raise ValidationError("Let's keep it classy. Please provide another name.")
        else:
            return name

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['submission', ]
