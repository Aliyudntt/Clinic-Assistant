from celery.decorators import task
from celery.utils.log import get_task_logger

from django.core.mail import EmailMessage,send_mail
from django.conf import settings

logger = get_task_logger(__name__)

@task(name="send_confirmation_email")
def send_confirmation_email(to, message, subject):
    logger.info("Sending Confirmation Email")

    message = EmailMessage(subject,message,settings.EMAIL_HOST_USER,[to])
    message.send()
    

@task(name="appointment_reminder")
def appointment_reminder(to,message,subject):
    logger.info("Sending Confirmation Email")

    message = EmailMessage(subject,message,settings.EMAIL_HOST_USER,[to])
    message.send()
    