# Generated by Django 3.1.1 on 2020-09-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpuspecs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpu',
            name='board_name',
            field=models.CharField(default='e4730', max_length=100),
            preserve_default=False,
        ),
    ]
