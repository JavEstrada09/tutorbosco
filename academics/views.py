from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from academics.forms import GradeForm, display_name
from academics.models import Enrollment, StudentProfile
from academics.services import (
    GradeRegistrationError,
    get_course_grade_sheet,
    get_course_summaries,
    get_taught_course,
    record_grade,
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
@require_http_methods(["GET", "POST"])
def teacher_course_grades(request, course_code):
    course = get_taught_course(request.user, course_code)
    if course is None:
        return render(request, "academics/access_denied.html", status=403)

    grade_sheet = get_course_grade_sheet(course)
    form = GradeForm(
        request.POST if request.method == "POST" else None,
        grade_sheet=grade_sheet,
    )
    registration_error = None
    status = 200
    if request.method == "POST":
        if form.is_valid():
            try:
                grade, created = record_grade(
                    user=request.user,
                    course=course,
                    student_pk=form.cleaned_data["student"],
                    topic_pk=form.cleaned_data["topic"],
                    value=form.cleaned_data["value"],
                )
            except GradeRegistrationError as error:
                registration_error = str(error)
            else:
                action = "Se guardó" if created else "Se actualizó"
                messages.success(
                    request,
                    f"{action} la nota {grade.value} de "
                    f"{display_name(grade.student.user)} en {grade.topic.name}.",
                )
                return redirect("teacher_course_grades", course_code=course.code)
        status = 400

    return render(
        request,
        "academics/teacher_course_grades.html",
        {
            "course": course,
            "form": form,
            "grade_sheet": grade_sheet,
            "registration_error": registration_error,
        },
        status=status,
    )
