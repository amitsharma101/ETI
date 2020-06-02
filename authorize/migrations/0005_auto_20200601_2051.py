# Generated by Django 3.0.6 on 2020-06-01 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authorize', '0004_fieldvalues_profilefields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldvalues',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authorize.ProfileFields'),
        ),
        migrations.AlterField(
            model_name='fieldvalues',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authorize.extendeduser'),
        ),
    ]