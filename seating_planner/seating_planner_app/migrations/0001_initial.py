# Generated by Django 2.2.1 on 2019-08-11 21:01

from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import jsonfield.fields
import seating_planner_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', django_enumfield.db.fields.EnumField(default=1, enum=seating_planner_app.models.Rank)),
                ('seq_num', models.IntegerField()),
                ('seat_num', models.IntegerField()),
                ('row_num', models.IntegerField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seating_planner_app.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('allocation', jsonfield.fields.JSONField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seating_planner_app.Section')),
            ],
            options={
                'unique_together': {('name', 'section')},
            },
        ),
    ]
