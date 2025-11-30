from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    reciever = models.ForeignKey(
        User,
        related_name='recieved_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False) 

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    
    
class MessageHistory(models.Model):
    """
    Stores older versions of a message before edits.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

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
