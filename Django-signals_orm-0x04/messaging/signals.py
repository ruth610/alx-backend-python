from django.db.models.signals import post_save,pre_save,post_delete
from .models import Message,Notification,MessageHistory,User
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

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before updating a message, store the old content in MessageHistory.
    """
    if instance.pk:  # Only run on update, not create
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        # Detect content change
        if old_message.content != instance.content:
            # Save old content to history
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True  # Mark message as edited

@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """
    After a User is deleted, clean up messages, notifications,
    and message histories related to them.
    """

    # Delete messages the user sent or received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to this user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where message belongs to the deleted user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()