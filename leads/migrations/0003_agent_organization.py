# Generated by Django 3.2.9 on 2021-12-02 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='organization',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
            preserve_default=False,
        ),
    ]
