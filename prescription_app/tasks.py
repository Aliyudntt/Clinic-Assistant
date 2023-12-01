from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import EmailMessage,send_mail
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task(name="send_prescription_email")
def send_prescription_email(pdf, to,date):
    logger.info("Sending Prescription Email")
    msg = "The following attachment is your prescription of your appoitnment on %s." %date
    message = EmailMessage("Prescription",msg,settings.EMAIL_HOST_USER,[to])
    message.attach("prescription.pdf", pdf,"application/pdf")    
    message.send()