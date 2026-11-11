import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from tutor.exercise_services import generate_practice, practice_state
from tutor.models import PracticeExercise
from tutor.providers import TutorError


@login_required
@require_http_methods(["GET", "POST"])
def student_practice(request, course_code):
    try:
        state = practice_state(request.user, course_code)
        if request.method == "POST":
            # El cliente solo solicita generar; propietario, tema y curso son del servidor.
            if set(request.POST) - {"csrfmiddlewaretoken"}:
                raise PermissionDenied
            try:
                _, notice = generate_practice(user=request.user, course_code=course_code)
                messages.info(request, notice)
            except TutorError as error:
                messages.error(request, str(error))
            return redirect("student_practice", course_code=course_code)

        exercises = PracticeExercise.objects.filter(
            student=state.student, course=state.summary.course,
        ).select_related("course", "topic")
        exercise_id = request.GET.get("exercise")
        if exercise_id is not None:
            try:
                exercise_id = uuid.UUID(exercise_id)
            except ValueError:
                raise PermissionDenied
            exercises = exercises.filter(pk=exercise_id)
            if not exercises.exists():
                raise PermissionDenied
        return render(request, "tutor/practice.html", {
            "state": state, "exercises": exercises[:6],
        })
    except PermissionDenied:
        return render(request, "academics/access_denied.html", status=403)
