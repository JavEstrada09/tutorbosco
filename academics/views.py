
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from academics.models import (
    Course,
    Enrollment,
    StudentProfile,
    TeacherProfile,
)
from academics.services import get_course_summaries
from tutor.demo_responses import DEMO_QUESTION
from tutor.forms import TutorQuestionForm
from tutor.providers import TutorError
from tutor.services import ask_tutor, get_tutor_mode

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from academics.models import Topic
from academics.teacher_forms import TopicForm
from academics.teacher_forms import StudentEnrollmentForm


@login_required
def student_home(request):
    enrollment = Enrollment.objects.select_related("student", "course").filter(
        student__user=request.user,
        course__code="PROG-COM",
    ).first()
    if enrollment is None:
        return render(request, "academics/access_denied.html", status=403)

    profile = enrollment.student
    continue_in_demo = request.POST.get("continue_in_demo") == "1"
    form_data = {"question": DEMO_QUESTION} if continue_in_demo else request.POST or None
    form = TutorQuestionForm(form_data)
    tutor_reply = None
    tutor_error = None
    offer_demo = False
    if request.method == "POST" and form.is_valid():
        try:
            tutor_reply = ask_tutor(
                question=form.cleaned_data["question"],
                career=profile.career,
                course_name=enrollment.course.name,
                mode="demo" if continue_in_demo else None,
            )
        except TutorError as error:
            tutor_error = str(error)
            offer_demo = True

    return render(
        request,
        "academics/student_home.html",
        {
            "career": profile.career,
            "course_name": enrollment.course.name,
            "demo_question": DEMO_QUESTION,
            "offer_demo": offer_demo,
            "tutor_mode": get_tutor_mode(),
            "tutor_error": tutor_error,
            "tutor_form": form,
            "tutor_reply": tutor_reply,
        },
    )


@login_required
@require_GET
def student_profile(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    if profile is None:
        return render(request, "academics/access_denied.html", status=403)

    return render(
        request,
        "academics/student_profile.html",
        {
            "full_name": request.user.get_full_name() or request.user.get_username(),
            "student_id": profile.student_id,
            "career": profile.career,
            "semester": profile.semester,
            "course_summaries": get_course_summaries(profile),
        },
    )


# ======================================================
# S-004: LISTADO DE CURSOS DEL DOCENTE
# Criterio de aceptación CA-1
# ======================================================

@login_required
@require_GET
def teacher_courses(request):
    """
    Muestra únicamente los cursos asignados al
    docente autenticado.

    Si el usuario no tiene perfil docente,
    responde con HTTP 403.
    """

    # Verificar que el usuario tenga perfil docente.
    is_teacher = TeacherProfile.objects.filter(
        user=request.user
    ).exists()

    if not is_teacher:
        return render(
            request,
            "academics/access_denied.html",
            status=403,
        )

    # Consultar los cursos impartidos por el docente.
    courses = (
        Course.objects.filter(
            teaching_assignments__teacher__user=request.user
        )
        .distinct()
        .order_by("code")
    )

    # Mostrar el listado de cursos.
    return render(
        request,
        "academics/teacher_courses.html",
        {
            "courses": courses,
            "show_grades_link": False,
        },
    )


# ======================================================
# S-004: GESTIÓN DE TEMAS ACADÉMICOS
# Criterios CA-2, CA-3, CA-4, CA-7 y CA-8
# ======================================================

@login_required
@require_http_methods(["GET", "POST"])
def teacher_course_topics(request, course_code):
    # Dependencia compartida con S-005.
    # Importación local hasta integrar su implementación.
    from academics.services import get_taught_course

    course = get_taught_course(request.user, course_code)

    if course is None:
        return render(
            request,
            "academics/access_denied.html",
            status=403,
        )

    topic_form = TopicForm(course=course)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            topic_form = TopicForm(
                request.POST,
                course=course,
            )

            if topic_form.is_valid():
                topic = topic_form.save(commit=False)
                topic.course = course
                topic.save()

                messages.success(
                    request,
                    "El tema académico se registró correctamente.",
                )

                return redirect(
                    "teacher_course_topics",
                    course_code=course.code,
                )

            messages.error(
                request,
                "Revise los datos del nuevo tema.",
            )

        elif action == "update":
            try:
                topic_id = int(request.POST.get("topic_id", ""))
            except (TypeError, ValueError):
                return render(
                    request,
                    "academics/access_denied.html",
                    status=403,
                )

            topic = Topic.objects.filter(
                pk=topic_id,
                course=course,
            ).first()

            if topic is None:
                return render(
                    request,
                    "academics/access_denied.html",
                    status=403,
                )

            update_form = TopicForm(
                request.POST,
                instance=topic,
                course=course,
            )

            if update_form.is_valid():
                update_form.save()

                messages.success(
                    request,
                    "El tema académico se actualizó correctamente.",
                )

                return redirect(
                    "teacher_course_topics",
                    course_code=course.code,
                )

            for errors in update_form.errors.values():
                for error in errors:
                    messages.error(request, str(error))

        else:
            messages.error(
                request,
                "La operación solicitada no es válida.",
            )

    topics = Topic.objects.filter(
        course=course,
    ).order_by("name", "pk")

    return render(
        request,
        "academics/teacher_course_topics.html",
        {
            "course": course,
            "topics": topics,
            "topic_form": topic_form,
        },
    )


# ======================================================
# S-004: ASIGNACIÓN DE ESTUDIANTES A CURSOS
# Criterios CA-5, CA-6, CA-7 y CA-8
# ======================================================

@login_required
@require_http_methods(["GET", "POST"])
def teacher_course_students(request, course_code):
    """
    Permite consultar y asignar estudiantes a los
    cursos impartidos por el docente autenticado.
    """

    # Función compartida desarrollada en S-005.
    from academics.services import get_taught_course

    course = get_taught_course(request.user, course_code)

    # Verificar que el docente imparta el curso.
    if course is None:
        return render(
            request,
            "academics/access_denied.html",
            status=403,
        )

    # Procesar la asignación de estudiantes.
    if request.method == "POST":
        student_form = StudentEnrollmentForm(
            request.POST,
            course=course,
        )

        action = request.POST.get("action")

        if action != "enroll":
            student_form.add_error(
                None,
                "La operación solicitada no es válida.",
            )

        elif student_form.is_valid():
            student = student_form.cleaned_data["student"]

            # Evitar registros duplicados.
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                course=course,
            )

            if created:
                messages.success(
                    request,
                    "El estudiante fue asignado correctamente.",
                )
            else:
                messages.warning(
                    request,
                    "El estudiante ya está asignado a este curso.",
                )

            return redirect(
                "teacher_course_students",
                course_code=course.code,
            )

    else:
        student_form = StudentEnrollmentForm(
            course=course,
        )

    # Consultar los estudiantes inscritos en el curso.
    enrollments = (
        Enrollment.objects.filter(
            course=course,
        )
        .select_related(
            "student",
            "student__user",
        )
        .order_by("student__student_id")
    )

    return render(
        request,
        "academics/teacher_course_students.html",
        {
            "course": course,
            "enrollments": enrollments,
            "student_form": student_form,
        },
    )
