from django.contrib import admin

from .models import Patient
from .models import Appointment

# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender','age', 'contact_number', 'email',)
    search_fields = ('name', 'contact_number', 'email')
    list_filter = ('gender', )


admin.site.register(Patient,PatientAdmin)
admin.site.register(Appointment)