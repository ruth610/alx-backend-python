from django.test import TestCase

from .models import Conversation, Message, User

# Create your tests here.

class MessageTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2',
            email='user2@example.com'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            password='password3',
            email='user3@example.com'
        )
        self.user4 = User.objects.create_user(
            username='user4',
            password='password4',
            email='user4@example.com'
        )

        self.conversation = Conversation.objects.create()
        self.conversation1 = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])
        self.conversation1.participants.set([self.user3, self.user4])

        Message.objects.create(
            sender=self.user1,
            conversation_id=self.conversation.id,
            message_body="Hello from user1 to user2"
        )
    def test_user_message_endpoint_only_retrieve_their_own_messages(self):
        self.client.login(username='user3', password='password3')

        response = self.client.get(f'/api/messages/?conversation_id={self.conversation.id}')

        self.assertEqual(response.status_code, 200) 