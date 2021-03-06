# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 07:16
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField(verbose_name='Body')),
                ('from_email', models.EmailField(max_length=254)),
                ('to', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, null=True), blank=True, editable=False, null=True, size=None)),
                ('bcc', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, null=True), blank=True, null=True, size=None)),
                ('cc', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, null=True), blank=True, null=True, size=None)),
                ('attachments', models.FileField(upload_to='', verbose_name='attachments')),
                ('reply_to', models.EmailField(blank=True, max_length=254, null=True)),
                ('announcement_type', models.CharField(choices=[('handout', 'Handout'), ('Assignment', 'Assignment')], max_length=30)),
                ('due_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_name', models.CharField(help_text='Assign a Group Name to the Student.', max_length=100, verbose_name='Group Name')),
                ('expiry_date', models.DateField(blank=True, help_text='Please Specify a validity period for the student group.', null=True, verbose_name='Expiry Date of the Student Group')),
                ('students_contact_csv', models.FileField(help_text="You can download the sample csv file <a href='/media/sample_contacts.csv'>here</a>", upload_to='', verbose_name='Contacts File')),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='study_group',
            field=models.ManyToManyField(to='Classroom.StudentGroup'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='email',
            name='study_group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Classroom.StudentGroup'),
        ),
    ]
