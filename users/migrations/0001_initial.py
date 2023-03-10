# Generated by Django 4.1.7 on 2023-02-24 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizUser',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('is_student', models.BooleanField()),
                ('is_verified', models.BooleanField(default=False)),
                ('otp', models.CharField(default='0', max_length=5)),
                ('number_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quizuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
