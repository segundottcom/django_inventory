# Generated by Django 3.2.12 on 2022-02-22 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0004_alter_stock_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockmgmt.category'),
        ),
    ]