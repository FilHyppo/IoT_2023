# Generated by Django 4.2.7 on 2023-11-09 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Idrometro',
            new_name='Igrometro',
        ),
        migrations.RenameModel(
            old_name='MasterIdrometri',
            new_name='MasterIgrometri',
        ),
    ]