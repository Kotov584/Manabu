# Generated by Django 4.1.5 on 2023-02-10 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='publication_date',
        ),
    ]
