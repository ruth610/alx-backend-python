from warnings import filters
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, User, Message
from .serializers import ConversationSerializers, MessageSerializers


# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()              # default queryset (fallback)
    serializer_class = ConversationSerializers        # serializer that handles validation and (de)serialization
    permission_classes = [IsAuthenticated]            # only logged-in users can access

    def get_queryset(self):
        user = self.request.user                       # the authenticated user making the request
        return Conversation.objects.filter(participants=user)  # only return conversations where the user participates
    
    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializers(data=request.data)  # bind incoming JSON to serializer
        serializer.is_valid(raise_exception=True)   # validate; if invalid -> 400 response automatically
        conversation = serializer.save()            # calls serializer.create() which writes to DB
        return Response(ConversationSerializers(conversation).data, status=201)  # return created data



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def get_queryset(self):
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = Message.objects.filter(conversation_id=conversation_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = MessageSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user)

        return Response(MessageSerializers(message).data,status=201)


