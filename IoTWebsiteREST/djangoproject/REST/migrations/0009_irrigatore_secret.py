# Generated by Django 4.2.10 on 2024-02-09 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0008_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='irrigatore',
            name='secret',
            field=models.CharField(default='password', max_length=16, unique=True),
            preserve_default=False,
        ),
    ]