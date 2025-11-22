from rest_framework.permissions import BasePermission
from .models import Conversation

class IsMessageOwnerOrParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Object-level permission: user must be the sender or a participant
        return (
            obj.sender == request.user or
            request.user in obj.conversation.participants.all()
        )

    def has_permission(self, request, view):
        conversation_id = request.query_params.get("conversation_id")
        if not conversation_id:
            return True  # allow post, list without convo ID (filtered in get_queryset)

        try:
            convo = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return False

        return request.user in convo.participants.all()
