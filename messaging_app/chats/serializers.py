from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializers(serializers.ModelSerializer):
    phone_number = serializers.CharField(allow_null=True, required=False)
    def  validate_password(self, password):
        if password.length < 8:
            raise serializers.ValidationError(
                'password must be greater or equal to 8 characters'
            )
        return password
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'role',
            'phone_number'
        ]


class MessageSerializers(serializers.ModelSerializer):
    sender = UserSerializers(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    def validate_message_body(self,message):
        if len(message.strip()) == 0:
            raise serializers.ValidationError(
                'message body can be an empty!!'
            )
        return message

    def validate(self, data):
        sender_id = data.get('sender_id')
        conversation = data.get('conversation')

        if not conversation.participants.filter(user_id = sender_id).exists():
            raise serializers.ValidationError(
                'the sender is not part of this conversation'
            )

        return data


    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_id',
            'conversation',
            'message_body',
            'sent_at'
        ]

class ConversationSerializers(serializers.ModelSerializer):
    participants = UserSerializers(many=True,read_only=True)
    participants_id = serializers.ListField(
        child =  serializers.UUIDField(),
        write_only=True
    )

    messages = MessageSerializers(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_id',
            'messages',
            'created_at'
        ]

    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids")
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        return conversation
