import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tutor", "0002_practiceexercise")]

    operations = [
        migrations.CreateModel(
            name="ExerciseAnswer",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("content", models.TextField(max_length=4000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("exercise", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="tutor.practiceexercise")),
            ],
            options={
                "ordering": ["-created_at", "id"],
                "indexes": [models.Index(fields=["exercise", "created_at"], name="answer_exercise_created_idx")],
            },
        ),
        migrations.CreateModel(
            name="ExerciseFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(max_length=10000)),
                ("source", models.CharField(choices=[("real", "IA"), ("demo", "Demo")], max_length=4)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("answer", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="tutor.exerciseanswer")),
            ],
            options={
                "constraints": [models.CheckConstraint(condition=models.Q(source__in=["real", "demo"]), name="exercise_feedback_valid_source")],
            },
        ),
    ]
