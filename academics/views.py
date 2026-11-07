from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from academics.models import StudentProfile


@login_required
def student_home(request):
    profile = StudentProfile.objects.filter(
        user=request.user,
        enrollments__course__code="PROG-COM",
    ).first()
    if profile is None:
        return render(request, "academics/access_denied.html", status=403)

    return render(
        request,
        "academics/student_home.html",
        {"career": profile.career},
    )
