# Generated by Django 4.1.3 on 2022-11-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='selected_number',
            field=models.IntegerField(default=-1),
        ),
    ]