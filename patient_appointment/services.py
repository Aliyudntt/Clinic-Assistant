from .tasks import send_confirmation_email
from .tasks import appointment_reminder


def send_confirmation_email_service(to, message, subject="do not reply"):
    send_confirmation_email.delay(to,message,subject)


def appointment_reminder_service(to,message,eta,subject="Appointment Reminder Notification"):
    appointment_reminder.apply_async(args=[to,message,subject], eta=eta)