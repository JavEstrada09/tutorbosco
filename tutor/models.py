import uuid

from django.db import models


class TutorConversation(models.Model):
    session = models.ForeignKey("sessions.Session", on_delete=models.CASCADE)
    student = models.ForeignKey("academics.StudentProfile", on_delete=models.CASCADE)
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE)
    academic_snapshot = models.JSONField(default=list)
    turns = models.JSONField(default=list)
    pending_question = models.CharField(max_length=500, blank=True, default="")
    revision = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("session", "student", "course"),
                name="unique_tutor_conversation_per_session_student_course",
            ),
        ]


class PracticeExercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey("academics.StudentProfile", on_delete=models.CASCADE)
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE)
    topic = models.ForeignKey("academics.Topic", on_delete=models.PROTECT)
    statement = models.TextField(max_length=3000)
    mode = models.CharField(max_length=4, choices=[("real", "IA"), ("demo", "Demo")])
    demo_key = models.CharField(max_length=80, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(mode__in=["real", "demo"]),
                name="practice_exercise_valid_mode",
            ),
        ]
