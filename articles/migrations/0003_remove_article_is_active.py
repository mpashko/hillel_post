# Generated by Django 3.1.6 on 2021-04-08 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_active',
        ),
    ]
