from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from tutor.models import TutorConversation


@receiver(user_logged_out, dispatch_uid="tutor.clear_logged_out_conversations")
def clear_logged_out_conversations(sender, request, **kwargs):
    session_key = request.session.session_key
    if session_key:
        TutorConversation.objects.filter(session_id=session_key).delete()
