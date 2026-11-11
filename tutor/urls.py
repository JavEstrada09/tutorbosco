from django.urls import path

from tutor.views import exercise_answer, exercise_answer_result


urlpatterns = [
    path(
        "practica/ejercicios/<uuid:exercise_id>/responder/",
        exercise_answer, name="exercise_answer",
    ),
    path(
        "practica/respuestas/<uuid:answer_id>/",
        exercise_answer_result, name="exercise_answer_result",
    ),
]
