import hashlib
import datetime

from django.db import models

from authentication.models import AuthUser
from authentication.models import Schedule

GENDER_CHOICES = [
    ('male', "MALE"),
    ('female', "FEMALE"),
]

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=14, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


APPOINTMENT_STATUS = [
    ('pending', "PENDING"),
    ('vistied', "VISITED"),
    ('cancelled', "CANCELLED"),
    ('absent', 'ABSENT')
]

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointment")
    doctor = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="appointment")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="appointment")
    date = models.DateField()
    status = models.CharField(max_length=9, choices=APPOINTMENT_STATUS, default='pending')
    secret = models.CharField(max_length=8,blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            key = self.patient.name + self.patient.contact_number
            self.secret = hashlib.md5(key.encode('utf-8')).hexdigest()[:8]
        super(Appointment,self).save(*args, **kwargs)

    def __str__(self):
        return self.patient.name




#
#model signals live here
#
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import send_confirmation_email_service
from .services import appointment_reminder_service

#post_save act to notify patient about appointment or on appointment cancellation
@receiver(post_save, sender=Appointment)
def send_appointment_notification(sender,instance, created, **kwargs):
    if created:
        #send sms code here
        #send email code here
        #queue cellery for reminder
        if instance.patient.email:
            to = instance.patient.email
            message = "Your apppointment is fixed with %s on %s at schedule %s-%s at %s branch." %(instance.doctor.name, instance.date, instance.schedule.start, instance.schedule.end, instance.schedule.branch_name)
            send_confirmation_email_service(to,message)
    else:
        if instance.status == "cancelled":
            #send sms code here
            #send email code here
            #remove from cellery task queue
            if instance.patient.email:
                to = instance.patient.email
                message = "Your apppointment with %s on %s at schedule %s-%s at %s branch is cancelled." %(instance.doctor.name, instance.date, instance.schedule.start, instance.schedule.end,instance.schedule.branch_name)
                send_confirmation_email_service(to,message)
        else:
            if instance.patient.email:
                to = instance.patient.email
                message = "Your apppointment with %s is rescheduled on %s at schedule %s-%s at %s branch." %(instance.doctor.name, instance.date, instance.schedule.start, instance.schedule.end,instance.schedule.branch_name)
                send_confirmation_email_service(to,message)
    
    if instance.status != "cancelled":
        if instance.patient.email:
            to = instance.patient.email
            message = "You have an appointment today with %s schedule: %s-%s at %s branch."%(instance.doctor.name, instance.date, instance.schedule.start, instance.schedule.end,instance.schedule.branch_name)
            date = datetime.datetime.combine(instance.date, instance.schedule.start)
            eta = date - datetime.timedelta(hours=2)
            appointment_reminder_service(to,message,eta)
           
    def get_absolute_url(self):
        return f"/appointment/{self.id}/"