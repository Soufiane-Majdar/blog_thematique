# Generated by Django 5.0.6 on 2024-06-29 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='image',
            field=models.ImageField(blank=True, upload_to='publications_imgs/'),
        ),
    ]
