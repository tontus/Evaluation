# Generated by Django 2.0.1 on 2018-02-13 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_auto_20180213_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='classroom.Student'),
        ),
    ]
