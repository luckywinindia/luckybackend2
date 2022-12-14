# Generated by Django 4.0.3 on 2022-09-30 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_profile_createdby'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recevier', to='mainapp.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.profile')),
            ],
        ),
    ]
