# Generated by Django 3.2.9 on 2021-12-07 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_auto_20211207_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
