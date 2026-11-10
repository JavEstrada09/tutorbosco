from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from academics.models import Course, Enrollment, StudentProfile, TeacherProfile
from academics.services import (
    get_course_panel,
    get_course_summaries,
    get_student_panel_row,
    get_taught_courses,
)
from tutor.demo_responses import DEMO_QUESTION
from tutor.forms import TutorQuestionForm
from tutor.providers import TutorError
from tutor.services import ask_tutor, get_tutor_mode


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
