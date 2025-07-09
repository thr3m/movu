import logging

from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger("apps")

def send_text_email(subject: str, message: str, recipient_list: list, from_email: str = None):
    """
    Sends a plain text email using Django's send_mail function.

    Args:
        subject (str): The subject line of the email.
        message (str): The plain text content of the email.
        recipient_list (list): A list of email addresses to send the email to.
        from_email (str, optional): The sender's email address. Defaults to settings.EMAIL_HOST_USER.
    """
    if not from_email:
        from_email = settings.EMAIL_HOST_USER

    try:
        
        #! implementation only for testing and showcase purposes
        # send_mail(
        #     subject,
        #     message,
        #     from_email,
        #     recipient_list,
        #     fail_silently=False,
        # )
        logger.info(f"Email '{subject}' sent successfully to {', '.join(recipient_list)}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email '{subject}' to {', '.join(recipient_list)}: {e}")
        return False

