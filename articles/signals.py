from time import sleep

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from sendgrid import Mail, SendGridAPIClient

from hillel_post.settings import EMAIL_SENDER, SENDGRID_KEY
from .config import SUSPICIOUS_WORDS
from .models import Comment, SuspiciousComment
from .tasks import send_email


@receiver(post_save, sender=Comment)
def mark_comment_as_suspicious(sender, instance, **kwargs):
    words = {w.lower() for w in instance.text.split(' ')}
    if words & SUSPICIOUS_WORDS:
        SuspiciousComment(comment=instance).save()
        Comment.objects.filter(id=instance.id).update(active=False)


# post_save.connect(
#     mark_comment_as_suspicious,
#     sender=Comment,
#     dispatch_uid='save_comment'
# )


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    task_id = send_email.delay(instance.to_dict())
