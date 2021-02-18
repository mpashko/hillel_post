from django.db.models.signals import post_save
from django.dispatch import receiver

from .config import SUSPICIOUS_WORDS
from .models import Comment, SuspiciousComment


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
