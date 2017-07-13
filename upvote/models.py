from django.db import models
from django.utils import timezone

class Submission(models.Model):
    word = models.CharField(max_length=50, unique=True)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super(Submission, self).save(*args, **kwargs)

class Vote(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    ip = models.CharField(max_length=300, null=True)