from django.contrib import admin

from .models import Medicine
from .models import Test
from .models import TestResult
from .models import MedicineRecommendations
from .models import TestResult
from .models import Prescription
from .models import History


#medincine Admin  class
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'preparation', 'manufacturer',  'added_by', 'created_at',]
    list_filter = ["manufacturer",]
    search_fields = ['medicine_name', 'preparation', 'manufacturer', 'created_at', 'added_by']
    exclude = ('added_by',)
    ordering = ["medicine_name",]
    
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'added_by', None) is None:
            obj.added_by = request.user
        obj.save()



#Test admin class
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'test_type', 'created_at', 'added_by')
    list_filter = ('test_type',)
    search_fields = ['test_name', 'test_type','added_by']
    exclude = ('added_by',)
    ordering = ['test_name',]


    def save_model(self, request, obj, form, change):
        if getattr(obj,'added_by', None) is None:
            obj.added_by = request.user
        obj.save()


#admin for TestResult
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('get_patient', 'get_dentist','test',  'created_at', 'result', 'unit', 'comment', 'created_at', 'diagnostic_center')
    list_filter = ('test',)
    search_fields = ['get_patient', 'get_dentist', 'test',]
    ordering = ['-created_at']

    def get_patient(self,obj):
        return obj.prescriptoin.history.patient.name

    def get_dentist(self,obj):
        return obj.prescription.history.dentist.name




#admin for prescription
class MedicineInline(admin.TabularInline):
    model = MedicineRecommendations
    extra = 1


class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 1


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['get_patient', 'get_dentist', 'created_at']
    search_fields = ['get_patient', 'get_dentist', 'created_at']
    ordering = ['-created_at',]
    inlines = [MedicineInline, TestResultInline]

    def get_patient(self,obj):
        return obj.history.patient.name

    def get_dentist(self,obj):
        return obj.history.dentist.name




#history admin 
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment_id', 'created_at']
    search_fields = ['patient', 'dentist', 'appointment_id']
    ordering = ['-created_at']

#register Admins to models
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestResult,TestResultAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(History,HistoryAdmin)