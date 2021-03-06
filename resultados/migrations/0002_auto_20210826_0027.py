# Generated by Django 3.2.6 on 2021-08-26 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas', '0001_initial'),
        ('resultados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultado',
            name='pregunta',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='preguntas.pregunta'),
        ),
        migrations.AddField(
            model_name='resultado',
            name='respuesta',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='preguntas.respuesta'),
        ),
    ]
