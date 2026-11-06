import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academics.models import Course, Enrollment, StudentProfile


DEMO_USERNAME = "estudiante_demo"
DEMO_STUDENT_ID = "2026-00001"
DEMO_CAREER = "Ingeniería en Sistemas"
DEMO_SEMESTER = 1
PILOT_COURSE_CODE = "PROG-COM"
PILOT_COURSE_NAME = "Programación Comercial"


class Command(BaseCommand):
    help = "Reconstruye los datos sintéticos mínimos de S-001."

    @transaction.atomic
    def handle(self, *args, **options):
        password = os.getenv("DEMO_STUDENT_PASSWORD")
        if not password:
            raise CommandError("DEMO_STUDENT_PASSWORD es obligatoria.")

        User = get_user_model()
        user = User.objects.select_for_update().filter(
            username=DEMO_USERNAME
        ).first()
        profile_for_id = StudentProfile.objects.select_for_update().filter(
            student_id=DEMO_STUDENT_ID
        ).first()

        if user:
            if user.is_staff or user.is_superuser:
                raise CommandError(
                    "La cuenta sintética existente tiene privilegios."
                )
            profile_for_user = StudentProfile.objects.select_for_update().filter(
                user=user
            ).first()
            if not profile_for_user or profile_for_user.student_id != DEMO_STUDENT_ID:
                raise CommandError(
                    "La cuenta sintética existente no coincide con el manifiesto."
                )
        else:
            profile_for_user = None

        if profile_for_id and (
            user is None or profile_for_id.user_id != user.pk
        ):
            raise CommandError(
                "El carné sintético ya pertenece a un perfil fuera del manifiesto."
            )

        if user is None:
            user = User(username=DEMO_USERNAME)
        user.first_name = "Estudiante"
        user.last_name = "Demo"
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if not user.check_password(password):
            user.set_password(password)
        user.save()

        profile = profile_for_user or profile_for_id
        if profile:
            profile.career = DEMO_CAREER
            profile.semester = DEMO_SEMESTER
            profile.save(update_fields=["career", "semester"])
        else:
            profile = StudentProfile.objects.create(
                user=user,
                student_id=DEMO_STUDENT_ID,
                career=DEMO_CAREER,
                semester=DEMO_SEMESTER,
            )
        course, _ = Course.objects.update_or_create(
            code=PILOT_COURSE_CODE,
            defaults={"name": PILOT_COURSE_NAME},
        )
        Enrollment.objects.get_or_create(student=profile, course=course)

        self.stdout.write(
            self.style.SUCCESS("Datos sintéticos mínimos reconstruidos.")
        )
