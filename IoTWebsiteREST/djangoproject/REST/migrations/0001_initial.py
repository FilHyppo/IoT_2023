# Generated by Django 4.2.7 on 2023-11-09 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterIdrometri',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('latitudine', models.FloatField()),
                ('longitudine', models.FloatField()),
                ('quota', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Idrometro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('latitudine', models.FloatField()),
                ('longitudine', models.FloatField()),
                ('ultima_misurazione', models.JSONField(blank=True, default=dict, null=True)),
                ('misurazioni', models.JSONField(blank=True, default=list, null=True)),
                ('attivo', models.BooleanField(default=False)),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='REST.masteridrometri')),
            ],
        ),
    ]