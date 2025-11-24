from warnings import filters
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, User, Message
from .serializers import ConversationSerializers, MessageSerializers
from .permissions import IsMessageOwnerOrParticipant
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()              # default queryset (fallback)
    serializer_class = ConversationSerializers        # serializer that handles validation and (de)serialization
    permission_classes = [IsAuthenticated]            # only logged-in users can access
    filterset_fields = ('messages')
    def get_queryset(self):
        user = self.request.user                       # the authenticated user making the request
        return Conversation.objects.filter(participants=user)  # only return conversations where the user participates
    
    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializers(data=request.data)  # bind incoming JSON to serializer
        serializer.is_valid(raise_exception=True)   # validate; if invalid -> 400 response automatically
        conversation = serializer.save()            # calls serializer.create() which writes to DB
        return Response(ConversationSerializers(conversation).data, status=201)  # return created data



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.order_by('pk')
    serializer_class = MessageSerializers
    permission_classes = [IsMessageOwnerOrParticipant]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param = 'size'
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['message_body']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user

        conversation_id = self.request.query_params.get('conversation_id')
        if not conversation_id:
            return Message.objects.none()

        # Ensure only participants can see messages
        return Message.objects.filter(
            conversation__id=conversation_id,
            conversation__participants=user
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.validated_data["conversation"]

        # Check user is in the conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=403
            )

        message = serializer.save(sender=request.user)

        return Response(
            MessageSerializers(message).data,
            status=201
        )
    def update(self, request, *args, **kwargs):
        message = self.get_object()

        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()

        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)


