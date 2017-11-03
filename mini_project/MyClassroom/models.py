from django.db import models
import uuid


# from django.core.mail import EmailMessage, send_mail
# from django.contrib.postgres.fields import ArrayField
# from django.apps import apps


class AssignmentSubmission(models.Model):
    """
    Assignment ChildClass. This class is the replica of the Master assignment class except it only enables a single field for Assignment Submission.
    """
    _id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subject = models.CharField(default="General",max_length=255)
    student = models.ForeignKey('Classroom.Student', on_delete=models.CASCADE, editable=False)
    master_assignment = models.ForeignKey('Classroom.MasterAssignment', on_delete=models.CASCADE, null=False)
    due_date = models.DateField(null=False, verbose_name="Due Date for the Assignment")
    assignment_attachement = models.FileField(verbose_name="Assignment Related Files")
    title = models.CharField(max_length=255)
    description = models.TextField(verbose_name='Description of the Assignment')
    special_instructions = models.TextField(verbose_name='Guidelines for the Assignment')
    submission_text = models.TextField(verbose_name="Assignment Submission",
                                       help_text="Write your Assignment Submission", null=True, blank=True)
    submission_attachment = models.FileField(verbose_name="Submission Attachment",
                                             help_text="For multiple file upload please make a zip file.")
    def __str__(self):
        return self.title


class Handout(models.Model):
    """
    Assignment ChildClass. This class is the replica of the Master assignment class except it only enables a single field for Assignment Submission.
    """
    _id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subject = models.CharField(default="General",max_length=255)
    student = models.ForeignKey('Classroom.Student', on_delete=models.CASCADE, editable=False)
    master_handout = models.ForeignKey('Classroom.MasterHandout', on_delete=models.CASCADE, null=False)
    handout_attachment = models.FileField(verbose_name="Handout Related Files")
    title = models.CharField(max_length=255)
    description = models.TextField(verbose_name='Description of the Assignment')
    def __str__(self):
        return self.title