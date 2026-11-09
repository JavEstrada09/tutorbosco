import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academics.models import (
    Course,
    Enrollment,
    Grade,
    StudentProfile,
    TeacherProfile,
    TeachingAssignment,
    Topic,
)


DEMO_USERNAME = "estudiante_demo"
DEMO_STUDENT_ID = "2026-00001"
DEMO_CAREER = "Ingeniería en Sistemas"
DEMO_SEMESTER = 1
PILOT_COURSE_CODE = "PROG-COM"
PILOT_COURSE_NAME = "Programación Comercial"

TOTAL_STUDENTS = 30
ADDITIONAL_COURSE_CODES = ("BD-APL", "DES-WEB", "REDES")
CAREERS = (
    "Ingeniería en Sistemas",
    "Administración de Empresas",
    "Contaduría Pública",
)

COURSE_BLUEPRINTS = {
    PILOT_COURSE_CODE: {
        "name": PILOT_COURSE_NAME,
        "topics": (
            "Git y GitHub avanzado",
            "Código limpio y refactoring",
            "Sistemas de información y bases de datos",
            "Ingeniería de prompts",
            "El LLM por dentro y su API",
            "Agentes de programación y desarrollo guiado por especificaciones",
        ),
    },
    "BD-APL": {
        "name": "Bases de Datos Aplicadas",
        "topics": (
            "Modelo relacional",
            "Consultas SQL",
            "Normalización",
            "Transacciones",
            "Índices y rendimiento",
            "Copias de seguridad y recuperación",
        ),
    },
    "DES-WEB": {
        "name": "Desarrollo Web",
        "topics": (
            "HTML semántico",
            "CSS y diseño adaptable",
            "JavaScript básico",
            "Formularios y validación",
            "Accesibilidad web",
            "Despliegue local",
        ),
    },
    "REDES": {
        "name": "Redes de Computadoras",
        "topics": (
            "Modelo OSI",
            "Direccionamiento IP",
            "Subredes",
            "Protocolos de transporte",
            "Seguridad básica de red",
            "Diagnóstico de conectividad",
        ),
    },
}

TEACHER_NAMES = {
    "docente_01": ("Ana", "Méndez"),
    "docente_02": ("Carlos", "López"),
    "docente_03": ("María", "Gómez"),
}
TEACHER_ASSIGNMENTS = {
    "docente_01": (PILOT_COURSE_CODE, "DES-WEB"),
    "docente_02": ("BD-APL",),
    "docente_03": ("REDES",),
}
DEMO_TEACHER_USERNAMES = tuple(TEACHER_NAMES)


class Command(BaseCommand):
    help = "Reconstruye el conjunto sintético completo de TutoBosco."

    @transaction.atomic
    def handle(self, *args, **options):
        student_password = os.getenv("DEMO_STUDENT_PASSWORD")
        if not student_password:
            raise CommandError("DEMO_STUDENT_PASSWORD es obligatoria.")

        teacher_password = os.getenv("DEMO_TEACHER_PASSWORD")
        if not teacher_password:
            raise CommandError("DEMO_TEACHER_PASSWORD es obligatoria.")

        User = get_user_model()
        self._validate_manifest(User)
        self._clear_managed_data()
        courses, topics = self._rebuild_courses()
        self._rebuild_teachers(User, teacher_password, courses)
        self._rebuild_students(
            User,
            student_password,
            courses,
            topics,
        )

        self.stdout.write(
            self.style.SUCCESS("Datos sintéticos completos reconstruidos.")
        )

    def _student_specs(self):
        specs = [
            {
                "username": DEMO_USERNAME,
                "student_id": DEMO_STUDENT_ID,
                "career": DEMO_CAREER,
                "semester": DEMO_SEMESTER,
                "additional_course": None,
                "no_grades": False,
            }
        ]
        for index in range(1, TOTAL_STUDENTS):
            username = f"estudiante_{index:02d}"
            specs.append(
                {
                    "username": username,
                    "student_id": f"2026-{index + 1:05d}",
                    "career": CAREERS[(index - 1) % len(CAREERS)],
                    "semester": ((index - 1) % 10) + 1,
                    "additional_course": ADDITIONAL_COURSE_CODES[
                        (index - 1) % len(ADDITIONAL_COURSE_CODES)
                    ],
                    "no_grades": username == "estudiante_02",
                }
            )
        return specs

    def _validate_manifest(self, User):
        for spec in self._student_specs():
            user = User.objects.filter(username=spec["username"]).first()
            if user is not None:
                self._reject_privileged_user(user)
                profile = StudentProfile.objects.filter(user=user).first()
                if (
                    profile is None
                    or profile.student_id != spec["student_id"]
                    or TeacherProfile.objects.filter(user=user).exists()
                ):
                    raise CommandError(
                        "La cuenta sintética existente no coincide con el manifiesto."
                    )

            profile_owner = StudentProfile.objects.filter(
                student_id=spec["student_id"]
            ).first()
            if (
                profile_owner is not None
                and profile_owner.user.username != spec["username"]
            ):
                raise CommandError(
                    "El carné sintético ya pertenece a un perfil fuera del manifiesto."
                )

        for username in DEMO_TEACHER_USERNAMES:
            user = User.objects.filter(username=username).first()
            if user is None:
                continue
            self._reject_privileged_user(user)
            has_teacher_profile = TeacherProfile.objects.filter(user=user).exists()
            has_student_profile = StudentProfile.objects.filter(user=user).exists()
            if has_student_profile or not has_teacher_profile:
                raise CommandError(
                    "La cuenta docente sintética existente no coincide "
                    "con el manifiesto."
                )

    def _reject_privileged_user(self, user):
        if user.is_staff or user.is_superuser:
            raise CommandError("La cuenta sintética existente tiene privilegios.")

    def _student_course_codes(self, spec):
        course_codes = [PILOT_COURSE_CODE]
        if spec["additional_course"]:
            course_codes.append(spec["additional_course"])
        return course_codes

    def _clear_managed_data(self):
        specs = self._student_specs()
        profiles = {
            profile.user.username: profile
            for profile in StudentProfile.objects.filter(
                user__username__in=[spec["username"] for spec in specs]
            ).select_related("user")
        }

        for spec in specs:
            profile = profiles.get(spec["username"])
            if profile is None:
                continue
            for course_code in self._student_course_codes(spec):
                Enrollment.objects.filter(
                    student=profile,
                    course__code=course_code,
                ).delete()
                if spec["no_grades"]:
                    continue
                Grade.objects.filter(
                    student=profile,
                    topic__course__code=course_code,
                    topic__name__in=COURSE_BLUEPRINTS[course_code]["topics"],
                ).delete()

        for username, course_codes in TEACHER_ASSIGNMENTS.items():
            TeachingAssignment.objects.filter(
                teacher__user__username=username,
                course__code__in=course_codes,
            ).delete()

    def _rebuild_courses(self):
        courses = {}
        topics = {}
        for code, blueprint in COURSE_BLUEPRINTS.items():
            course, _ = Course.objects.update_or_create(
                code=code,
                defaults={"name": blueprint["name"]},
            )
            courses[code] = course
            topics[code] = {}
            for topic_name in blueprint["topics"]:
                topics[code][topic_name] = Topic.objects.update_or_create(
                    course=course,
                    name=topic_name,
                )[0]
        return courses, topics

    def _rebuild_teachers(self, User, password, courses):
        for username in DEMO_TEACHER_USERNAMES:
            first_name, last_name = TEACHER_NAMES[username]
            user = self._upsert_user(
                User,
                username,
                first_name,
                last_name,
                password,
            )
            teacher, _ = TeacherProfile.objects.update_or_create(user=user)
            for course_code in TEACHER_ASSIGNMENTS[username]:
                TeachingAssignment.objects.create(
                    teacher=teacher,
                    course=courses[course_code],
                )

    def _rebuild_students(self, User, password, courses, topics):
        for index, spec in enumerate(self._student_specs()):
            user = self._upsert_user(
                User,
                spec["username"],
                "Estudiante",
                "Demo" if index == 0 else f"{index:02d}",
                password,
            )
            profile, _ = StudentProfile.objects.update_or_create(
                user=user,
                defaults={
                    "student_id": spec["student_id"],
                    "career": spec["career"],
                    "semester": spec["semester"],
                },
            )

            course_codes = self._student_course_codes(spec)

            for course_code in course_codes:
                Enrollment.objects.create(
                    student=profile,
                    course=courses[course_code],
                )

            if spec["no_grades"]:
                continue

            for course_code in course_codes:
                for topic_index, topic_name in enumerate(
                    COURSE_BLUEPRINTS[course_code]["topics"]
                ):
                    Grade.objects.create(
                        student=profile,
                        topic=topics[course_code][topic_name],
                        value=self._grade_value(
                            index,
                            topic_index,
                            spec["username"],
                        ),
                    )

    def _upsert_user(self, User, username, first_name, last_name, password):
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if not user.check_password(password):
            user.set_password(password)
        user.save()
        return user

    def _grade_value(self, student_index, topic_index, username):
        if username == DEMO_USERNAME:
            return (55, 58, 90, 92, 88, 85)[topic_index]
        if student_index == 1:
            return 70 + ((topic_index * 3) % 21)
        return 50 + ((student_index * 7 + topic_index * 11) % 46)
