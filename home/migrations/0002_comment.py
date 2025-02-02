# Generated by Django 4.1.2 on 2022-12-23 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_comment', to='home.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='home.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='your_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
