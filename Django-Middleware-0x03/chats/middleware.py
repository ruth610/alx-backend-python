from datetime import datetime, timedelta
import logging
from django.http import HttpResponse, HttpResponseForbidden

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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allowed between 6AM (06) and 9PM (21)
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden("Access to the messaging app is restricted at this time.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store timestamps of requests per IP
        self.ip_message_log = {}

        # Rate limit configuration
        self.TIME_WINDOW = timedelta(minutes=1)  # 1 minute window
        self.MAX_MESSAGES = 5  # max 5 messages per minute

    def __call__(self, request):
        # Apply limit only to POST requests (sending messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list for IP if not present
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []

            # Filter out old timestamps outside the 1-minute window
            self.ip_message_log[ip] = [
                t for t in self.ip_message_log[ip]
                if now - t < self.TIME_WINDOW
            ]

            # Check rate limit
            if len(self.ip_message_log[ip]) >= self.MAX_MESSAGES:
                return HttpResponse(
                    "Rate limit exceeded: You can only send 5 messages per minute.",
                    status=429
                )

            # Log current message timestamp
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')