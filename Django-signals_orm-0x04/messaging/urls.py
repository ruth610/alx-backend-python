from django.urls import path
from .views import delete_user,unread_messages

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path("unread/", unread_messages, name="unread_messages"),
]