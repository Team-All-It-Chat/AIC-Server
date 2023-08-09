# Generated by Django 4.2.4 on 2023-08-08 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField(blank=True, max_length=300, null=True)),
                ('answer', models.TextField(blank=True, max_length=2000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('question_time', models.DateTimeField(blank=True, null=True)),
                ('answer_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('answerer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_as_answerer', to=settings.AUTH_USER_MODEL, verbose_name='답변자')),
                ('questioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_as_questioner', to=settings.AUTH_USER_MODEL, verbose_name='질문자')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, max_length=500, null=True)),
                ('sent_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('chat_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='message.chat')),
            ],
        ),
    ]
