from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from tutor.demo_feedback import demo_case
from tutor.feedback import owned_answer, owned_exercise, submit_answer
from tutor.forms import ExerciseAnswerForm


def _answer_page(request, exercise, *, form=None, answer=None):
    return render(request, "tutor/exercise_answer.html", {
        "exercise": exercise,
        "answer_form": form if form is not None else ExerciseAnswerForm(),
        "answer": answer,
        "feedback": getattr(answer, "feedback", None) if answer else None,
        "attempts": exercise.answers.select_related("feedback"),
        "demo_case": demo_case(exercise),
    })


@login_required
@require_http_methods(["GET", "POST"])
def exercise_answer(request, exercise_id):
    try:
        exercise = owned_exercise(request.user, exercise_id)
        form = ExerciseAnswerForm(request.POST if request.method == "POST" else None)
        if request.method == "POST":
            if set(request.POST) - {"content", "csrfmiddlewaretoken"}:
                raise PermissionDenied
            if form.is_valid():
                answer, notice = submit_answer(
                    user=request.user, exercise_id=exercise.pk,
                    content=form.cleaned_data["content"],
                )
                messages.info(request, notice)
                return redirect("exercise_answer_result", answer_id=answer.pk)
        return _answer_page(request, exercise, form=form)
    except PermissionDenied:
        return render(request, "academics/access_denied.html", status=403)


@login_required
@require_GET
def exercise_answer_result(request, answer_id):
    try:
        answer = owned_answer(request.user, answer_id)
        return _answer_page(request, answer.exercise, answer=answer)
    except PermissionDenied:
        return render(request, "academics/access_denied.html", status=403)
