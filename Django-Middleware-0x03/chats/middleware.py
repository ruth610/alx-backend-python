from datetime import datetime
import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")      # log file in project root
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        self.logger.info(
            f"{datetime.now()} - User: {user} - Path: {request.path}"
        )

        response = self.get_response(request)
        return response