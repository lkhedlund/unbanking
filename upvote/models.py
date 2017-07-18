from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.text import slugify

from .utils import format_word

class Submission(models.Model):
    letters = RegexValidator(r'^[a-zA-Z\s]*$', 'Only letters and spaces are allowed.')

    name = models.CharField(max_length=50, validators=[letters])
    word = models.CharField(max_length=25, unique=True, validators=[letters])
    published_date = models.DateTimeField(default=timezone.now)
    disabled = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.word)

        self.word = format_word(self.word)
        super(Submission, self).save(*args, **kwargs)

class Vote(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return "Added on {date}".format(date=self.submission_date)