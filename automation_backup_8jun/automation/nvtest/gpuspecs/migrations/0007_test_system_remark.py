# Generated by Django 3.1.3 on 2021-02-16 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpuspecs', '0006_auto_20201006_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_system',
            name='Remark',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]