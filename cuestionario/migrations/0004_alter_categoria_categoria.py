# Generated by Django 3.2.6 on 2021-09-01 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuestionario', '0003_auto_20210828_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='categoria',
            field=models.CharField(max_length=300),
        ),
    ]