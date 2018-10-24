from .tasks import send_prescription_email

def send_prescription(pdf,patient, date):
    if patient.email:
        send_prescription_email.delay(pdf,patient.email,date)    