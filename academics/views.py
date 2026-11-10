from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from academics.models import Enrollment, StudentProfile
from academics.services import get_course_summaries
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
