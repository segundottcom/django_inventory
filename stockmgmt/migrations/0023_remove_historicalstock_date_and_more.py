# Generated by Django 4.0.4 on 2022-05-24 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0022_alter_historicalstock_issue_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalstock',
            name='date',
        ),
        migrations.RemoveField(
            model_name='historicalstock',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='historicalstock',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='historicalstock',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='date',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='timestamp',
        ),
    ]
