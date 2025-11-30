from django.db.models.signals import post_save
from .models import Message,Notification
from django.dispatch import receiver


@receiver(post_save,sender=Message)
def create_message_notification(sender,instance,created,**kwargs):
    """
    When a new message is created, automatically generate
    a notification for the receiver.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            Message=instance
        )
        