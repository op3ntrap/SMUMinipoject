from django.contrib import admin
from .models import *
from django.utils.html import format_html
from datetime import date


# Register your models here.
@admin.register(AssignmentSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ['master_assignment', 'due_date', 'title', 'description', 'special_instructions',
                       '_Assignment_Attachment']
    exclude = ['assignment_attachement']
    list_filter = ['subject', 'due_date', 'student']
    list_display_links = ['title','student']
    ordering = ['due_date']
    list_display = ['title', 'student', 'due_date']

    def _Assignment_Attachment(self, obj=None):
        if obj.due_date > date.today():
            return format_html(
                    '<div class="file-path-wrapper"><a class="input-field-action" href="{}" target="blank" title="catalog_scraper.py"><i class="material-icons">file_download</i>Download Assignment Attachment Files</a></div>',
                    obj.assignment_attachement.url)
        else:
            return '<div class="row"><div class="checkbox-field col s12"> <input type="checkbox" id="test7" checked="checked" disabled="disabled"> <label for="test7">Due Date has Passed</label></div></div>'

    def get_queryset(self, request):
        qs = super(SubmissionAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(student=request.user.student)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['master_assignment', 'due_date', 'title', 'description', 'special_instructions', 'subject',
                           '_Assignment_Attachment']
        if obj.due_date < date.today():
            readonly_fields.extend(['submission_text'])

        return readonly_fields

        # def get_exclude(self, request, obj=None):
        # exclude = ['assignment_attachement']
        # if obj.due_date < date.today():
        #     exclude.extend(['submission_attachement',])
        # return exclude


@admin.register(Handout)
class HandoutAdmin(admin.ModelAdmin):
    readonly_fields = ['master_handout', 'title', 'description', '_Handout_Attachment', 'subject']
    exclude = ['handout_attachment']
    list_display_links = ['title','student']
    list_filter = ['subject', 'student']
    list_display = ['title', 'student']

    def _Handout_Attachment(self, obj=None):
        # if obj.due_date > date.today():
        return format_html(
                '<div class="file-path-wrapper"><a class="input-field-action" href="{}" target="blank" title="catalog_scraper.py"><i class="material-icons">file_download</i>Download Handout Attachment Files</a></div>',
                obj.handout_attachment.url)

    def get_queryset(self, request):
        qs = super(HandoutAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(student=request.user.student)

