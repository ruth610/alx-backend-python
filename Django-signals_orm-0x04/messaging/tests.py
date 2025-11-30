
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class SignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="123")
        self.receiver = User.objects.create_user(username="receiver", password="123")

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )

        # A notification should be created automatically
        notifications = Notification.objects.filter(user=self.receiver)

        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, message)
