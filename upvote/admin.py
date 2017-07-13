from django.contrib import admin

from .models import Submission, Vote

class VoteInline(admin.TabularInline):
    model = Vote

class SubmissionAdmin(admin.ModelAdmin):
    inlines = [VoteInline]
    list_display = ['word']
    search_fields = ['word']

admin.site.register(Submission, SubmissionAdmin)
