from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UnreadMessagesManager(models.Manager):
    """
    Custom manager to get unread messages for a specific user.
    Optimized with .only() to load minimal fields.
    """
    def unread_for_user(self, user):
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")  # Optimization
        )


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # NEW FIELD
    read = models.BooleanField(default=False)

    # DEFAULT MANAGER
    objects = models.Manager()

    # CUSTOM UNREAD MANAGER
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:20]}"
    

class MessageHistory(models.Model):
    """
    Stores older versions of a message before edits.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        related_name='message_edited_by',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
    

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID {self.message.id}"


