# Generated by Django 2.2.4 on 2019-08-29 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_list_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(1, 'New'), (2, 'Done')], default=1, max_length=1),
        ),
    ]