from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import EmailMessage
from DCA import settings

logger = get_task_logger(__name__)

@shared_task(name="send_confirmation_email")
def send_confirmation_email(to, message, subject):
    logger.info("Sending Confirmation Email")

    try:
        email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to])
        email_message.send()
        logger.info("Confirmation Email sent successfully")
    except Exception as e:
        logger.error(f"Error while sending Confirmation Email: {str(e)}")

@shared_task(name="appointment_reminder")
def appointment_reminder(to, message, subject):
    logger.info("Sending Appointment Reminder")

    try:
        email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to])
        email_message.send()
        logger.info("Appointment Reminder sent successfully")
        return "done"
    except Exception as e:
        logger.error(f"Error while sending Appointment Reminder: {str(e)}")