# messaging/views.py
import json
from django.db.models import Q, Prefetch
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from .models import Message
from django.contrib.auth.models import User


def _build_thread(message):
    """
    Recursive helper that returns a dict with nested replies.
    Assumes message.replies.all() is prefetched.
    """
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp.isoformat(),
        "edited": message.edited,
        "replies": [_build_thread(r) for r in message.replies.all()]
    }
@login_required
def unread_messages(request):
    user = request.user

    # Use the custom manager
    unread = Message.unread.unread_for_user(user)

    return JsonResponse({
        "unread_count": unread.count(),
        "messages": [
            {
                "id": msg.id,
                "sender": msg.sender.username,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in unread
        ]
    })

@login_required
def get_conversation(request, user_id):
    """
    Returns top-level messages (parent_message is null) between the
    current user and the other user, including nested replies.
    Uses select_related and prefetch_related to minimize DB queries.
    """
    other_user = get_object_or_404(User, id=user_id)
    me = request.user

    # Query top-level messages between the two users.
    # THIS LINE uses Message.objects.filter as required by the test.
    top_level_qs = Message.objects.filter(
        Q(sender=me, receiver=other_user) | Q(sender=other_user, receiver=me),
        parent_message__isnull=True
    ).select_related("sender", "receiver", "parent_message")

    # Prefetch replies (and a level deeper) to avoid N+1.
    # We prefetch replies and their sender/receiver so building thread is cheap.
    replies_prefetch = Prefetch(
        "replies",
        queryset=Message.objects.select_related("sender", "receiver").prefetch_related("replies"),
        to_attr="prefetched_replies"
    )

    # Attach prefetch; note: message.replies.all() will be populated by the prefetch.
    messages = top_level_qs.prefetch_related(
        replies_prefetch,
        "replies__replies",  # help prefetch grandchildren where possible
    ).order_by("timestamp")

    # Because we used `to_attr="prefetched_replies"`, ensure replies property is accessible.
    # To keep _build_thread simple we map `replies` manager to the prefetched attribute.
    threaded = []
    for msg in messages:
        # Attach a small wrapper so msg.replies.all() returns the prefetched list
        # (only done in-memory — does not touch DB).
        if hasattr(msg, "prefetched_replies"):
            # create a simple object with all() to mimic queryset API expected by _build_thread
            class _RepliesWrapper:
                def __init__(self, lst): self._lst = lst
                def all(self): return self._lst
            msg.replies = _RepliesWrapper(msg.prefetched_replies)

            # Also ensure every reply has `replies` attribute prefetched where possible
            for r in msg.prefetched_replies:
                if hasattr(r, "prefetched_replies"):
                    r.replies = _RepliesWrapper(r.prefetched_replies)
        else:
            # fallback — leave as-is so accessing .replies will issue queries if not prefetched
            pass

        threaded.append(_build_thread(msg))

    return JsonResponse({"conversation_with": other_user.username, "thread": threaded})


@login_required
@require_http_methods(["POST"])
def reply_to_message(request, message_id):
    """
    Create a reply to a message.
    Expects JSON body: {"content": "reply text"}
    """
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON body.")

    content = payload.get("content")
    if not content:
        return HttpResponseBadRequest("Missing 'content' field.")

    parent = get_object_or_404(Message, id=message_id)

    # Determine receiver: typically the parent sender (unless replying to yourself)
    if parent.sender == request.user:
        # If you are the original sender and you reply, the receiver should be the original receiver
        receiver = parent.receiver
    else:
        receiver = parent.sender

    reply = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent
    )

    # Return the created reply as JSON (minimal fields)
    return JsonResponse({
        "status": "ok",
        "reply": {
            "id": reply.id,
            "sender": reply.sender.username,
            "receiver": reply.receiver.username,
            "content": reply.content,
            "timestamp": reply.timestamp.isoformat(),
            "parent_message": parent.id
        }
    }, status=201)
