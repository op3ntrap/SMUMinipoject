from django.db import models
from django.contrib.auth.models import User, Group
import uuid, csv
from django.apps import apps
from django.core.mail import EmailMessage, send_mail
from django.contrib.postgres.fields import ArrayField
import string
import random


# Create your models here.


class StudentGroup(models.Model):
    """
    Model Class of Student Groups
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=100, verbose_name="Group Name",
                                  help_text="Assign a Group Name to the Student.", unique=True)

    expiry_date = models.DateField(null=True, blank=True, verbose_name="Expiry Date of the Student Group",
                                   help_text="Please Specify a validity period for the student group.")
    students_contact_csv = models.FileField(verbose_name="Contacts File",
                                            help_text="You can download the sample csv file <a href='/media/sample_contacts.csv'>here</a>",
                                            null=True)
    created_date = models.DateField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):

        def passworder(self):

            chars = string.ascii_letters + string.digits

            pwdSize = 10
            return ''.join((random.choice(chars)) for x in range(pwdSize))

        def send_welcome_email(self, first_name=None, last_name=None, email=None, password=None, username=None):
            """
                        Method to send Welcome Email with Login Credentials.
                        :param first_name:
                        :param last_name:
                        :param email:
                        :param password:
                        :param username:
                        :return:
                        """
            body = "Hi {} {},\n You're teacher has created your account on Classroom. You can login at htttp://127.0.0.1/admin using the following credentials.\n " \
                   "Username:{} \n Password:{} \n\n Thanks!".format(first_name, last_name, username, password)
            send_mail('Welcome To Classroom: Login Credentials', body, 'classroom@gmail.com', recipient_list=[email],
                      fail_silently=True)
            return 0

        def namer(x):
            chars = string.ascii_letters + string.digits

            pwdSize = 3
            return x.join((random.choice(chars)) for x in range(pwdSize))

        def join_students(self):
            if self.students_contact_csv is not None:
                with open(self.students_contact_csv.path, 'r') as data_file:
                    dump = csv.DictReader(data_file)
                    student_thread = apps.get_model('Classroom', model_name='Student')
                    for row in dump:
                        # create user
                        passwd = passworder(self)
                        # create user and profile if the student does not exist in backend.
                        if len(User.objects.filter(username=row['email'])) == 0:
                            member = User.objects.create(first_name=row['first_name'], last_name=row['last_name'],
                                                         email=row['email'],
                                                         password=passwd, username=namer(row['first_name']), is_staff=True)
                            # assign_student_permissions
                            member.groups.add(Group.objects.get(name='Student'))
                            member.save()
                            # create student
                            profile = student_thread.objects.create(user=member, study_group=(self,))
                            send_welcome_email(self, first_name=row['first_name'], last_name=row['last_name'],
                                               email=row['email'],
                                               password=passwd, username=row['email'], )
                        else:
                            profile = User.objects.get(email=row['email'])
                            # assign_student_permissions
                            profile.groups.add(Group.objects.get(name='Student'))
                            profile.student.study_group.add(self)

        super(StudentGroup, self).save(*args, **kwargs)
        join_students(self)

    def __str__(self):
        return self.group_name


class Student(models.Model):
    """
    Student model Class
    """

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    study_group = models.ManyToManyField(StudentGroup)

    def __str__(self):
        return self.user.first_name + self.user.last_name


class Email(models.Model):
    """
    Model Class for all Email Communications. It also handles the Email Backend of this Module.
    """
    ANNOUNCEMENT_TYPE = (
        ('handout', 'Handout'),
        ('Assignment', 'Assignment'),
    )
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mail = EmailMessage()
    subject = models.CharField(max_length=200)
    body = models.TextField(verbose_name="Body")
    from_email = models.EmailField()
    to = ArrayField(models.EmailField(null=True, blank=True), null=True, blank=True, editable=False)
    bcc = ArrayField(models.EmailField(null=True, blank=True), null=True, blank=True, )
    cc = ArrayField(models.EmailField(null=True, blank=True), null=True, blank=True, )
    attachments = models.FileField(verbose_name="attachments")
    reply_to = models.EmailField(null=True, blank=True)
    announcement_type = models.CharField(choices=ANNOUNCEMENT_TYPE, max_length=30)
    due_date = models.DateField(null=True, blank=True)
    study_group = models.OneToOneField(StudentGroup, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        models.Model.save() function override.
        Sends out the email when the template is saved.
        :param args:
        :param kwargs:
        :return:
        """

        def send_group_mail(self):
            """
            Method to Send Email using django.core.mail.EmailMessage as service.
            SMTP configurations exist in the settings.py file.
            :param self:
            :return:
            """
            mailer = EmailMessage(subject=self.subject, body=self.body, from_email=self.from_email)
            # Adding recipient Email Addresses from the student groups.
            self.to = []
            group_members = Student.objects.filter(study_group=self.study_group)
            for member in group_members:
                self.to.append(str(member.user.email))
            mailer.to = self.to
            other_email_fields = [mailer.bcc, mailer.cc, mailer.reply_to]
            model_form_fields = [self.bcc, self.cc, self.reply_to]
            for other_field, model_field in zip(other_email_fields, model_form_fields):
                if model_field is not None:
                    other_field = model_field
            # Attach file if the an attachment was provided.
            if self.attachments is not None:
                mailer.attach_file(self.attachments.path)
            sent = mailer.send(fail_silently=False)

        send_group_mail(self)
        super(Email, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject + "[{}]".format(self.announcement_type)


class MasterAssignment(models.Model):
    """
    Assignment Master Class. This class enables the Teachers to create an Assignment Object for the student to submit.
    """
    _id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    student_group = models.ManyToManyField(StudentGroup)
    due_date = models.DateField(null=False, verbose_name="Due Date for the Assignment")
    assignment_attachement = models.FileField(verbose_name="Assignment Related Files")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(verbose_name='Description of the Assignment')
    special_instructions = models.TextField(verbose_name='Guidelines for the Assignment')
    subject=models.CharField(max_length=255, default="General")


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        def create_student_submission_object(self):
            """
            Creates MyClassroom.AssignmentSubmission Objects for each student.

            :param self:
            """
            submission = apps.get_model('MyClassroom', model_name='AssignmentSubmission')
            assigned_student_groups = self.student_group.all()  # QuerySet
            # For each of the student in the student group an assignment submission object has to be created.
            for student_group in assigned_student_groups:
                # List of students
                students = student_group.student_set.all()
                for student in students:
                    submission.objects.create(
                            master_assignment=self,
                            due_date=self.due_date,
                            assignment_attachement=self.assignment_attachement,
                            title=self.title,
                            description=self.description,
                            special_instructions=self.special_instructions,
                            student=student,
                            subject=self.subject

                    )
        super(MasterAssignment, self).save(*args, **kwargs)
        create_student_submission_object(self)

class MasterHandout(models.Model):
    """
    Assignment Master Class. This class enables the Teachers to create an Assignment Object for the student to submit.
    """
    _id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    student_group = models.ManyToManyField(StudentGroup)
    handout_attachment = models.FileField(verbose_name="Assignment Related Files")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(verbose_name='Description of the Assignment')
    subject=models.CharField(max_length=255, default="General")


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        def create_student_handout_object(self):
            """
            Creates MyClassroom.AssignmentSubmission Objects for each student.

            :param self:
            """
            handout = apps.get_model('MyClassroom', model_name='Handout')
            assigned_student_groups = self.student_group.all()  # QuerySet
            # For each of the student in the student group an assignment submission object has to be created.
            for student_group in assigned_student_groups:
                # List of students
                students = student_group.student_set.all()
                for student in students:
                    handout.objects.create(
                            master_handout=self,
                            handout_attachment=self.handout_attachment,
                            title=self.title,
                            description=self.description,
                            student=student,
                            subject=self.subject

                    )
        super(MasterHandout, self).save(*args, **kwargs)
        create_student_handout_object(self)
