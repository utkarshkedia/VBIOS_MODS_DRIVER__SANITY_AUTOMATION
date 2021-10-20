# Generated by Django 3.1.1 on 2020-10-03 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpuspecs', '0003_gpu_rom_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login_Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test_System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100)),
                ('Operating_System', models.CharField(max_length=100)),
            ],
        ),
    ]
