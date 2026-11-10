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
