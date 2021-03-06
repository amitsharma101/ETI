# Generated by Django 3.0.6 on 2020-06-01 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authorize', '0003_auto_20200530_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FieldValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorize.ProfileFields')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorize.extendeduser')),
            ],
        ),
    ]
