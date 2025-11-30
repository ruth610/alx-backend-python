from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from .models import User,Message
from django.views.decorators.csrf import csrf_exempt

@login_required
def delete_user(request):
    """
    Allows a user to delete their account.
    """
    user = request.user
    logout(request)        # Log out first
    user.delete()          # Trigger deletion (signals included)
    return redirect('/')   # Redirect to home page


def get_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # fetch all top-level messages (parent_message=None) between both users
    messages = (
        Message.objects
        .filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user],
            parent_message__isnull=True
        )
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related(
            "replies",
            "replies__sender",
            "replies__receiver",
            "replies__replies",  # prefetch grandchildren
        )
        .order_by("timestamp")
    )

    # Build threaded tree
    threaded = [build_thread(m) for m in messages]

    return JsonResponse({"conversation": threaded})

@csrf_exempt
def reply_to_message(request, message_id):
    if request.method == "POST":
        parent = get_object_or_404(Message, id=message_id)
        content = request.POST.get("content")

        reply = Message.objects.create(
            sender=request.user,
            receiver=parent.receiver,
            content=content,
            parent_message=parent
        )

        return JsonResponse({"status": "ok", "reply_id": reply.id})
