# Generated by Django 3.2.8 on 2022-03-25 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='viwes',
            new_name='views',
        ),
    ]