from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Student, StudentGroup, Email, MasterAssignment, MasterHandout)
class ClassroomAdmin(admin.ModelAdmin):
    pass