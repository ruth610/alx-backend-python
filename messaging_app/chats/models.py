import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.TextChoices):
    GUEST = ['Guest','guest']
    HOST = ['Host','host']
    ADMIN = ['Admin','admin']


class User(AbstractUser):
    """
    Extends Django AbstractUser because the default User model
    already includes: username, first_name, last_name, email, password
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.BigIntegerField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST
    )
    created_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email',
    USERNAME_FIELD = 'username',
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    participants = models.ManyToManyField(
        User,
        related_name='participants'
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sender = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.conversation.id}"





