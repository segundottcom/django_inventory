# Generated by Django 4.0.4 on 2022-07-03 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0025_expenses_historicalstock_net_sales_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstock',
            name='expense',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='expense',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
