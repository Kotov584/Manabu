from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, AcademicYear
import uuid
import os


def get_file_path(instance, filename): 
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/', filename)

class Assignment(models.Model): 
    title = models.CharField(max_length=255)
    content = models.TextField()
    courses = models.ManyToManyField(Course)
    due_date = models.DateTimeField()
    status = models.IntegerField()


    def __str__(self):
        return self.title

class UserAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    grade = models.CharField(max_length=255, null=True, blank=True)
    level = models.CharField(max_length=255) 
    result = models.CharField(max_length=255)
    credit = models.CharField(max_length=255)
    attempt = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.assignment.title}'
