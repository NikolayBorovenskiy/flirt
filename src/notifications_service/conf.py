from django.conf import settings


MESSAGING_REDIS_HOST = getattr(settings, 'MESSAGING_REDIS_HOST', 'localhost')
MESSAGING_REDIS_PORT = getattr(settings, 'MESSAGING_REDIS_PORT', 6379)
MESSAGING_REDIS_CHANNEL = getattr(settings, 'MESSAGING_REDIS_CHANNEL', 'message_notifications')
