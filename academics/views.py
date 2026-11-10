from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from academics.models import (
    Course,
    Enrollment,
    StudentProfile,
    TeacherProfile,
    Topic,
)
from academics.services import (
    get_course_panel,
    get_course_summaries,
    get_student_panel_row,
    get_taught_courses,
)
from academics.teacher_forms import StudentEnrollmentForm, TopicForm
from tutor.demo_responses import DEMO_QUESTION
from tutor.forms import TutorQuestionForm
from tutor.providers import TutorError
from tutor.services import ask_tutor, get_tutor_mode


@login_required
@require_http_methods(["GET", "POST"])
def student_home(request):
    enrollments = list(
        Enrollment.objects.select_related("student", "course")
        .filter(student__user=request.user)
        .order_by("course__name", "course__code")
    )
    if not enrollments:
        return render(request, "academics/access_denied.html", status=403)

    course_code = request.POST.get("course", request.GET.get("course"))
    by_code = {item.course.code: item for item in enrollments}
    if course_code is None:
        enrollment = by_code.get("PROG-COM", enrollments[0])
    else:
        enrollment = by_code.get(course_code)
        if enrollment is None:
            return render(request, "academics/access_denied.html", status=403)

    profile = enrollment.student
    tutor_mode = get_tutor_mode()
    demo_question = DEMO_QUESTION if enrollment.course.code == "PROG-COM" else None
    continue_in_demo = request.POST.get("continue_in_demo") == "1"
    form_data = {"question": demo_question} if continue_in_demo else request.POST or None
    form = TutorQuestionForm(form_data)
    tutor_reply = None
    tutor_error = None
    offer_demo = False
    if request.method == "POST":
        if not demo_question and (continue_in_demo or tutor_mode == "demo"):
            tutor_error = "El modo demo aún no tiene respuestas grabadas para este curso."
        elif form.is_valid():
            try:
                tutor_reply = ask_tutor(
                    question=form.cleaned_data["question"],
                    career=profile.career,
                    course_name=enrollment.course.name,
                    mode="demo" if continue_in_demo else None,
                )
            except TutorError as error:
                if demo_question:
                    tutor_error = str(error)
                    offer_demo = True
                else:
                    tutor_error = (
                        "No fue posible obtener una respuesta del tutor. "
                        "El modo demo aún no tiene respuestas grabadas para este curso."
                    )

    return render(
        request,
        "academics/student_home.html",
        {
            "career": profile.career,
            "courses": [item.course for item in enrollments],
            "selected_course": enrollment.course,
            "demo_question": demo_question,
            "offer_demo": offer_demo,
            "tutor_mode": tutor_mode,
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


@login_required
@require_GET
def role_home(request):
    """Redirige tras el inicio de sesión según el perfil de la cuenta.

    Un usuario con perfil estudiantil conserva el comportamiento de
    S-001 y va a la pantalla del estudiante; uno solo docente va al
    panel del docente; sin perfil recibe 403.
    """
    if StudentProfile.objects.filter(user=request.user).exists():
        return redirect("student_home")
    if TeacherProfile.objects.filter(user=request.user).exists():
        return redirect("teacher_panel")
    return render(request, "academics/access_denied.html", status=403)


def _get_taught_course(user, course_code):
    """Devuelve el curso si el usuario es docente que lo imparte, o None."""
    teacher = TeacherProfile.objects.filter(user=user).first()
    if teacher is None:
        return None
    return Course.objects.filter(
        code=course_code,
        teaching_assignments__teacher=teacher,
    ).first()


def _order_panel_rows(rows, order):
    """Ordena las filas del panel por promedio según el parámetro recibido.

    Sin orden válido conserva el orden por nombre del servicio. Los
    estudiantes sin notas quedan al final en ambos sentidos.
    """
    if order not in ("promedio-asc", "promedio-desc"):
        return list(rows)
    with_average = [row for row in rows if row.average is not None]
    without_average = [row for row in rows if row.average is None]
    with_average.sort(
        key=lambda row: row.average, reverse=order == "promedio-desc"
    )
    return with_average + without_average


@login_required
@require_GET
def teacher_panel(request):
    teacher = TeacherProfile.objects.filter(user=request.user).first()
    if teacher is None:
        return render(request, "academics/access_denied.html", status=403)

    return render(
        request,
        "academics/teacher_panel.html",
        {"courses": get_taught_courses(teacher)},
    )


@login_required
@require_GET
def teacher_course_panel(request, course_code):
    course = _get_taught_course(request.user, course_code)
    if course is None:
        return render(request, "academics/access_denied.html", status=403)

    panel = get_course_panel(course)
    order = request.GET.get("orden", "")
    return render(
        request,
        "academics/teacher_course_panel.html",
        {
            "course": course,
            "rows": _order_panel_rows(panel.rows, order),
            "topic_weak_counts": panel.topic_weak_counts,
            "order": order,
        },
    )


@login_required
@require_GET
def teacher_student_detail(request, course_code, student_id):
    course = _get_taught_course(request.user, course_code)
    if course is None:
        return render(request, "academics/access_denied.html", status=403)

    student = StudentProfile.objects.filter(
        pk=student_id,
        enrollments__course=course,
    ).first()
    if student is None:
        return render(request, "academics/access_denied.html", status=403)

    return render(
        request,
        "academics/teacher_student_detail.html",
        {
            "course": course,
            "row": get_student_panel_row(course, student),
        },
    )
