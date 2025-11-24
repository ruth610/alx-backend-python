from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Object-level permission: user must be the sender or a participant
        conversation = obj.conversation if isinstance(obj, Message) else obj

        # Only participants allowed for all modifying methods
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in conversation.participants.all()

        return False

    def has_permission(self, request, view):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # For list/create — check conversation_id if provided
        conversation_id = request.query_params.get("conversation_id") or \
                          request.data.get("conversation")

        if not conversation_id:
            # Allow auth user but queryset will restrict data anyway
            return True

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return False

        return request.user in conversation.participants.all()
