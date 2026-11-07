from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    student_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{4}-\d{5}$",
                message="El carné debe usar el formato AAAA-NNNNN.",
            )
        ],
    )
    career = models.CharField(max_length=120)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(semester__gte=1, semester__lte=10),
                name="student_semester_between_1_and_10",
            )
        ]

    def __str__(self):
        return self.student_id


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_enrollment",
            )
        ]

    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )

    def __str__(self):
        return self.user.get_username()


class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="teaching_assignments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="teaching_assignments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "course"],
                name="unique_teacher_course_assignment",
            )
        ]

    def __str__(self):
        return f"{self.teacher} - {self.course.code}"


class Topic(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    name = models.CharField(max_length=150)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "name"],
                name="unique_course_topic_name",
            )
        ]

    def __str__(self):
        return f"{self.course.code} - {self.name}"


class Grade(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="grades",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="grades",
    )
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "topic"],
                name="unique_student_topic_grade",
            ),
            models.CheckConstraint(
                condition=models.Q(value__gte=0, value__lte=100),
                name="grade_value_between_0_and_100",
            ),
        ]

    def __str__(self):
        return f"{self.student.student_id} - {self.topic.name}: {self.value}"
