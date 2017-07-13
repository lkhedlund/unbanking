from django import forms
from .models import Submission, Vote

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['word', ]