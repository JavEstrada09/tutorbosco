import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0002_teacherprofile_teachingassignment_topic_grade"),
        ("tutor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PracticeExercise",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("statement", models.TextField(max_length=3000)),
                ("mode", models.CharField(choices=[("real", "IA"), ("demo", "Demo")], max_length=4)),
                ("demo_key", models.CharField(blank=True, default="", max_length=80)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="academics.course")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="academics.studentprofile")),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="academics.topic")),
            ],
            options={
                "ordering": ["-created_at", "id"],
                "constraints": [models.CheckConstraint(condition=models.Q(mode__in=["real", "demo"]), name="practice_exercise_valid_mode")],
            },
        ),
    ]
