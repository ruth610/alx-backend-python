def build_thread(message):
    """
    Recursively builds a threaded structure of messages and replies.
    """
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "edited": message.edited,
        "replies": [build_thread(reply) for reply in message.replies.all()]
    }
