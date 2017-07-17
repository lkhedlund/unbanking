from django.contrib import admin

from .models import Submission, Vote

class VoteInline(admin.StackedInline):
    model = Vote
    extra = 1

class SubmissionAdmin(admin.ModelAdmin):
    def vote_count(self, obj):
        return obj.vote_set.count()

    inlines = [VoteInline]
    list_display = ['word', 'published_date', 'disabled', 'vote_count', 'name']
    search_fields = ['word', 'name']

admin.site.register(Submission, SubmissionAdmin)
