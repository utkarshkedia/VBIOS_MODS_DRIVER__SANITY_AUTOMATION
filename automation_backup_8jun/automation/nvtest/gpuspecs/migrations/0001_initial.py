# Generated by Django 3.1.1 on 2020-09-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_the_gpu', models.CharField(max_length=100)),
                ('memory_type', models.CharField(max_length=100)),
            ],
        ),
    ]
