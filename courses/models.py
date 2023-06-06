from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, default="")

    class Meta:
        verbose_name_plural = "categories" 

    def __str__(self):
        return f'{self.name}'

class AcademicYear(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    start_year = models.TextField()
    end_year = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Course(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True, default="")
    name = models.CharField(max_length=255, blank=True, null=True, default="") 
    comments = models.CharField(max_length=255, blank=True, null=True, default="") 
    description = models.TextField(blank=True, null=True, default="") 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='courses')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Topic(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return f'{self.title}'
