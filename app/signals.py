# app/signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f'User {user.username} logged in from IP {request.META.get("REMOTE_ADDR", "unknown")}')
    print(f'User {user.username} logged in from IP {request.META.get("REMOTE_ADDR", "unknown")}')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f'User {user.username} logged out')
    print(f'User {user.username} logged out')
