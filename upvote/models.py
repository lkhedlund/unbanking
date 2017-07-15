from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from upvote.data.profanity import profanity_set
from .utils import format_word

def validate_profanity(word):
    if word in profanity_set:
        raise ValidationError("Let's keep this classy, please.")

class Submission(models.Model):
    letters = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')

    word = models.CharField(max_length=50, unique=True, validators=[letters, validate_profanity])
    published_date = models.DateTimeField(default=timezone.now)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.word

    def clean(self, *args, **kwargs):
        validate_profanity(self.word)
        super(Submission, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()
        self.word = format_word(self.word)
        super(Submission, self).save(*args, **kwargs)

class Vote(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return "Added on {date}".format(date=self.submission_date)