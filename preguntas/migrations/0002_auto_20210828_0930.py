# Generated by Django 3.2.6 on 2021-08-28 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='texto',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='texto',
            field=models.CharField(max_length=300),
        ),
    ]
