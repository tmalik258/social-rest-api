# Generated by Django 5.0.7 on 2024-08-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('users', '0002_user_posts_liked_alter_user_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='posts_liked',
            field=models.ManyToManyField(related_name='liked_by', to='posts.post'),
        ),
    ]
