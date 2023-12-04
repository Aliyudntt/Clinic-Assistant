import datetime


from django.db import models


from authentication.models import AuthUser
from patient_appointment.models import Patient
from patient_appointment.models import Appointment



#model for medicine
class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100,unique=True)
    preparation = models.DecimalField(max_digits=5, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    medicine_description = models.TextField()
    added_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.medicine_name



TEST_TYPE_CHOICES = [
    (1,'Test Result is numerical'),
    (2,'Test Result is categorical'),
    (3, 'Test Result contains attachment')
]


class Test(models.Model):
    test_name = models.CharField(max_length=100)
    test_type = models.IntegerField(choices=TEST_TYPE_CHOICES)
    created_at = models.DateField(auto_now=True)
    added_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.test_name


TEST_RESULT_UNIT_CHOICES = [
    ('pH', 'pH'),
    ('mg/dL', 'mg/dL'),
    ('units/L', 'units/L'),
    ('mEq/dL', 'mEq/dL'),
    ('%', "%"),
    ( u"cells/\u03BCL" ,u"cells/\u03BCL"),
    (u'\u03BCg/L',u'\u03BCg/L' ),
]






#class General Information
class History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="history")
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="history")
    doctor = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='history')
    weight = models.PositiveIntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    pulse = models.PositiveIntegerField(blank=True, null=True)
    blood_pressure = models.CharField(max_length=10,blank=True, null=True)
    respiratory_disease = models.BooleanField(default=False)
    cardiovascular_disease = models.BooleanField(default=False)
    hepatobiliary_disease = models.BooleanField(default=False)
    viral_hepatitis_disease = models.BooleanField(default=False)
    nurological_disease = models.BooleanField(default=False)
    tb_disease = models.BooleanField(default=False)
    diabetes_disease = models.BooleanField(default=False)
    rheumatic_fever_disease = models.BooleanField(default=False)
    drug_allergy_disease = models.BooleanField(default=False)
    pregnancy_disease = models.BooleanField(default=False)
    blood_disease = models.BooleanField(default=False)
    surgical_history_disease = models.BooleanField(default=False)
    drug_history_disease = models.BooleanField(default=False)
    allergic_history_disease = models.BooleanField(default=False)
    endodontic_examination = models.CharField(max_length=100, blank=True, null=True)
    tooth_number =  models.CharField(max_length=30, blank=True, null=True)
    type_of_affection = models.CharField(max_length=100, blank=True, null=True)
    presence_of_pain = models.CharField(max_length=30, blank=True, null=True)
    measure_of_pain = models.CharField(max_length=30, blank=True, null=True)
    time_posture_of_pain = models.CharField(max_length=30, blank=True, null=True)
    duration_of_pain = models.CharField(max_length=30, blank=True, null=True)
    pain_initiated_by = models.CharField(max_length=30, blank=True, null=True)
    pain_relieved_by = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.patient.name 

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "Histories"


#model for Prescription
class Prescription(models.Model):
    history = models.OneToOneField(History, on_delete=models.CASCADE, related_name='prescription')
    recommended_tests = models.ManyToManyField(Test)
    created_at = models.DateTimeField(auto_now=True)




#test Result
class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='test_result')
    unit = models.CharField(max_length=10,choices=TEST_RESULT_UNIT_CHOICES, blank=True, null=True)
    result = models.CharField(max_length=100,blank=True,null=True)
    attachment = models.FileField(upload_to='test_results/', blank=True, null=True)
    diagnostic_center = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient.name 
    
    def save(self, *args, **kwargs):
        if not self.pk and self.attachment:
            ext = self.attachment.name.split('.')[-1]
            self.attachment.name = "%d_%s.%s" %(self.patient.id, str(datetime.datetime.now), ext)
        super(TestResult,self).save(*args,**kwargs)

    class Meta:
        verbose_name = "Test Result"
        verbose_name_plural = "Test Results"





class MedicineRecommendations(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='recommended_medicines')
    dosage_interval = models.PositiveIntegerField()
    comments = models.CharField(max_length=100, null=True, blank=True)
    dosage_qty = models.PositiveIntegerField(default=1)


    def get_dosage_str(self):
        interval = int(24/self.dosage_interval)
        
        ret =  "+".join([str(self.dosage_qty) for i in range(interval)])
        
        return ret

