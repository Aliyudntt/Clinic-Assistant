import json


from django.db.models import F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect


from .models import Medicine
from .models import Test
from .models import History
from .models import Prescription
from .models import MedicineRecommendations
from .models import TestResult


from patient_appointment.models import Appointment


@login_required
def medicinelist(request):
    return render(
                    request,
                    "prescription_app/medicine_list.html", 
                    {'medicines': Medicine.objects.all().order_by('medicine_name')}
                )


@login_required
def medicine_add(request):
    if request.method == "POST":
        medicine_name = request.POST.get('medicine_name')
        preparation = request.POST.get('preparation')
        manufacturer = request.POST.get('manufacturer')
        medicine_description = request.POST.get('medicine_description')
        

        medicine, created = Medicine.objects.get_or_create( 
                                        added_by=request.user,
                                        medicine_name=medicine_name,
                                        preparation=preparation,
                                        manufacturer=manufacturer,
                                        medicine_description=medicine_description
                                        )

        if created:
            messages.success(request, "Successfully added  medcine: " + medicine_name + " " + str(preparation) + "mg")
        
        return HttpResponseRedirect("/prescription/medicines/")

    return render(request, "prescription_app/medicine_add.html",{})



#Test Lists
@login_required
def testlist(request):
    return render(
        request, 
        "prescription_app/test_list.html",
        {'tests': Test.objects.all().order_by('test_name')}
        )



#test add
@login_required
def test_add(request):
    if request.method == "POST":
        test_name = request.POST.get('test_name')
        test_type = int(request.POST.get('test_type'))

        obj, created = Test.objects.get_or_create(
            test_name=test_name,
            test_type = test_type,
            added_by = request.user
        )

        if created:
            messages.success(request, "Successfully added test: " + test_name)
        return HttpResponseRedirect("/prescription/tests/")

    return render(request, "prescription_app/test_add.html",)


#prescription creation
@login_required
def prescription_add(request, appointment_id):
    if request.method=="POST":
        print(request.POST.dict())
        recommended_test_list = request.POST.getlist('tests')
        recommended_test_list = [int(i) for i in recommended_test_list]
        data = request.POST.dict()
        data.pop('tests',None)
        appointment = None
        try:
            appoinment = Appointment.objects.prefetch_related().get(id=appointment_id)
        except:
            messages.error("Error: The appointment does not exist")
            return HttpResponseRedirect("/appoinment/all/")
        
        medicine_dict = {}
        test_result_dict = {}
        for key in list(data):
            if key.startswith('medicine_'):
                medicine_dict[key] = data.get(key)
                del data[key]
            elif key.startswith('test_'):
                test_result_dict[key] = data.get(key)
                del data[key]
            elif data[key] == 'on':
                data[key] = True
            elif data[key] == '':
                data[key] = None

        data.pop('csrfmiddlewaretoken')

        recommended_medicine_list = {}
        for key in medicine_dict:
            idx = key.split("_")[-1]
            recommended_medicine_list[idx] = {}
            for jkey in medicine_dict:
                if jkey.endswith("_"+idx):
                    newKey = jkey.replace("_"+idx, '')
                    recommended_medicine_list[idx][newKey] = medicine_dict[jkey]

        
        test_reuslt_list = {}
        for key in test_result_dict:
            idx = key.split("_")[-1]
            test_reuslt_list[idx] = {}
            for jkey in test_result_dict:
                if jkey.endswith("_"+idx):
                    newKey = jkey.replace("_"+idx,'')
                    test_reuslt_list[idx][newKey] = test_reuslt_dict[jkey]
        
       
        
        history = History(**data)
        history.patient = appoinment.patient
        history.appointment = appoinment
        history.dentist = request.user
        history.save()
        
        prescription = Prescription()
        prescription.history = history
        prescription.save()
        prescription.recommended_tests.add(*recommended_test_list)
        prescription.save()
        

        for key in recommended_medicine_list:
            medicine = recommended_medicine_list[key]
            try:
                MedicineRecommendations.objects.create(
                    medicine_id = medicine.get('medicine_name'),
                    prescription = prescription,
                    dosage_interval = medicine.get('medicine_dosage_interval'),
                    comments = medicine.get('medicine_comments'),
                    dosage_qty = medicine.get('medicine_dosage_qty')
                )
            except:
                pass

        for key in test_reuslt_list:
            test_result = test_reuslt_list[key]
            try:
                TestResult.objects.create(
                    test_id = test_result['test_id'],
                    presacription = prescription,
                    unit = test_result['test_unit'],
                    result = test_result['test_result'],
                    attachment = request.Files['test_attachment_'+key],
                    comments = test_result['test_comment'],
                    diagnostic_center = test_result['test_diagnostic_center']
                )
            except:
                pass
       
        history.appointment.status = "visited"
        history.appointment.save()

        messages.success(request,"Successfully created Patient history")
        return HttpResponseRedirect('/prescription/history/'+str(history.id)+"/")
        
    tests = Test.objects.all()
    medicines = Medicine.objects.all()
    return render(request,"prescription_app/prescription.html",{'appointment_id' : appointment_id,'tests': tests, 'medicines': medicines})


#history detail
@login_required
def history_detail(request, id):
    history = None
    
    try:
        history = History.objects.get(id=id,dentist=request.user)
    except:
        messages.error(request,"Error: You are not authorized to view this history")
        return HttpResponseRedirect('/prescription/history/')
    
    return render(request, 'prescription_app/history_detail.html', {'history': history})


@login_required
def historylist(request):
    histories = History.objects.prefetch_related().filter(dentist=request.user)
    return render(request,"prescription_app/history_list.html",{'histories':histories})



import datetime
from io import BytesIO
from reportlab.pdfgen import canvas, textobject
from reportlab.lib.units import inch
from django.http import HttpResponse


from .services import send_prescription

@login_required
def to_pdf(request,id):
    history = None
    try:
        history = History.objects.get(dentist=request.user, id=id)
    except:
        messages.error(request,"Error: You are not authorized to view this history")
        return HttpResponseRedirect('/prescription/history/')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="prescription_%d_%s.pdf"'%(history.patient.id,str(datetime.datetime.now()))
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawCentredString(300,800, "Confident Dental Care")
    
    patient = history.patient
    prescription = history.prescription
    dentist = history.dentist

    patientString = '''Name: %s
Age:%s 
Gender: %s
Contact Number: %s
%s
'''%(patient.name, patient.age, patient.gender, patient.contact_number, str(datetime.datetime.now()))

    textobject = p.beginText()
    textobject.setTextOrigin(inch, inch*10.5)
    textobject.textLines(patientString)
    
    dentistString = '''Dentist: %s
    %s
    Contact: %s
    Email: %s
'''%(dentist.name, dentist.about, dentist.contact_number,dentist.email)

    textobject.moveCursor(inch*4.5,inch*-1)
    textobject.textLines(dentistString)
    textobject.moveCursor(inch*-4.5, inch*.5)
    textobject.textLine("Rx,")
    
    count = 1
    for medicine in prescription.recommended_medicines.all():
        textobject.moveCursor(inch*1,inch*.1)
        medString = "%d. %s : %s %s"%(count,medicine.medicine.medicine_name, medicine.get_dosage_str(), medicine.comments)
        textobject.textLine(medString)
        count +=1

    if prescription.recommended_tests.count() > 0:
        textobject.moveCursor(inch*1,inch*.15)
        textobject.textLine("Recommended Tests")
        count = 1
        for test in prescription.recommended_tests.all():
            textobject.moveCursor(inch*1,inch*.1)
            testString = "%d. %s" %(count,test.test_name)
            textobject.textLine(testString) 
            count += 1
    p.drawText(textobject)



    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    send_prescription(pdf,patient,prescription.created_at)

    return response