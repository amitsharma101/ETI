# Generated by Django 3.0.6 on 2020-05-30 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorize', '0002_extendeduser_lid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendeduser',
            name='phone_num',
        ),
        migrations.RemoveField(
            model_name='extendeduser',
            name='semester',
        ),
    ]
