from django.db.models.signals import post_save
from django.dispatch import receiver

from .config import SUSPICIOUS_WORDS
from .models import Comment, SuspiciousComment


# @receiver(post_save, sender=Comment)
def add_suspicious_comment(sender, instance, **kwargs):
    words = {w.lower() for w in instance.body.split(' ')}
    if words & SUSPICIOUS_WORDS:
        SuspiciousComment(comment=instance).save()
        Comment.objects.filter(id=instance.id).update(active=False)


post_save.connect(
    add_suspicious_comment,
    sender=Comment,
    dispatch_uid='save_comment'
)
