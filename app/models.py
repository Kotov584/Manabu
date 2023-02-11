from django.db import models

class Book(models.Model):
    db_table = 'app_book'
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    #publication_date = models.DateField() 