import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.models import User


from authentication.models import AuthUser
from authentication.models import Schedule


from .models import Patient
from .models import Appointment

# Create your views here.
@csrf_exempt
def schedule_appointmet(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        email = request.POST.get('email',"")
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number').replace(' ', '').replace('-', '')
        dentist = int(request.POST.get('dentist'))
        schedule = int(request.POST.get('schedule'))
        date = datetime.datetime.strptime(request.POST.get('date'), "%m/%d/%Y").date()
        
        patient = None

        schedule_object = Schedule.objects.get(id=schedule)

        if Appointment.objects.filter(schedule__id=schedule, date=date).count() >= schedule_object.max_patient:
            return render(request, 'patient_appointment/appointment_confirm.html',{'error': True, 'message':"Sorry, your selected schedule is full. Please try another schedule"})

        if date == datetime.date.today() and schedule_object.start < datetime.datetime.now().time():
            return render(request, 'patient_appointment/appointment_confirm.html',{'error': True, 'message': "Sorry, Your selected schedule has passed today. Please try another schedule"})
        try:
            patient = Patient.objects.get(contact_number=contact_number)
            return render(request, 'patient_appointment/appointment_confirm.html', {'error':True, 'message': 'Patient with contact number: <em>' + patient.contact_number + "</em> is already registered. Please try with a different contact number" })
        except:
            patient = Patient.objects.create(
                name=name,
                age = age,
                email = email,
                gender = gender,
                contact_number = contact_number
            )

            appointment = Appointment.objects.create(
                date = date,
                patient_id = patient.id,
                dentist_id = dentist,
                schedule_id = schedule
            )

            return render(request,"patient_appointment/appointment_confirm.html", {'error': False,'patient': patient, 'appointment': appointment})
    return render(request, "patient_appointment/appointment_confirm.html", {"error": True, 'message': 'Please go back to <a href="/">Home</a> page to make an appointment'})




@csrf_exempt
def schedule_list(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        branch = request.POST.get('branch')

        print(request.POST)
        
        dentists_set = set(
            User.objects.filter(
                Q(schedule__weekday=day) &
                Q(schedule__branch_name=branch) &
                Q(is_active=True) &
                Q(is_superuser=False)
            ).prefetch_related('schedule')
        )

        if len(dentists_set) == 0:
            return JsonResponse({'message': "Sorry, no dentist is available"}, status=404)

        dentists = []

        for dentist in dentists_set:
            schedules = dentist.schedule.filter(
                Q(weekday=day) | Q(weekday='All'),
                branch_name=branch
            ).values('id', 'start', 'end', 'weekday')

            dentist_data = {
                'id': dentist.id,
                'name': dentist.get_full_name(),
                'schedules': list(schedules)
            }

            dentists.append(dentist_data)

        return JsonResponse({'data': dentists})

    return JsonResponse({'message': 'Invalid request'}, status=400)


#list appointments of a doctor
@login_required
def today_appointments(request):
    appointments = Appointment.objects.prefetch_related().filter(dentist=request.user, date=datetime.date.today()).order_by('-created_at',)
    return render(request,'dashboard/appointment_list.html', {'appointments':appointments,'headline':"Today's Appointments"})



#list all upcoming pending appointments
@login_required
def upcoming_appointments(request):
    appointments = Appointment.objects.prefetch_related().filter(dentist=request.user,status="pending").order_by('-created_at',)
    return render(request,'dashboard/appointment_list.html', {'appointments':appointments,'headline':"Upcoming Appointments"})


#list all appointments of a doctor
@login_required
def all_appointment(request):
    appointments = Appointment.objects.prefetch_related().filter(dentist=request.user).order_by('-created_at',)
    return render(request,'dashboard/appointment_list.html', {'appointments':appointments,'headline':"All Appointments"})


#search appointment by contact number
@login_required
def search_appointment_by_contact_numer(request):
    contact_number = request.POST.get('search_param').replace(' ', '').replace('-', '')    
    appointments = Appointment.objects.prefetch_related().filter(dentist=request.user, patient__contact_number=contact_number)
    return render(request,'dashboard/appointment_list.html', {'appointments':appointments,'headline':"Search Results"})


#create unregistered appointment on the fly by dentist
@login_required
def unregistered_appointment(request):
    if request.method=="POST":
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        email = request.POST.get('email',"")
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number').replace(' ', '').replace('-', '')
        dentist = request.user.id
        schedule = int(request.POST.get('schedule'))
        date = datetime.datetime.strptime(request.POST.get('date'), "%m/%d/%Y").date()
        

        patient = None

        schedule_object = Schedule.objects.get(id=schedule)

        if Appointment.objects.filter(schedule__id=schedule, date=date).count() >= schedule_object.max_patient:
            messages.warning(request,"No slot is empty at the selected schedule")
            return HttpResponseRedirect("/appointment/dentist/add/")

        if date == datetime.date.today() and schedule_object.start < datetime.datetime.now().time():
            messages.error(request, "Selected schedule has passed for today")
            return HttpResponseRedirect("/appointment/dentist/add/")

        try:
            patient = Patient.objects.get(contact_number=contact_number)
            messages.error(request, "A patient is already registered with contact number" + contact_number + " Try a different contact number")
            return HttpResponseRedirect("/appointment/dentist/add/")

        except:
            patient = Patient.objects.create(
                name=name,
                age = age,
                email = email,
                gender = gender,
                contact_number = contact_number
            )

            appointment = Appointment.objects.create(
                date = date,
                patient_id = patient.id,
                dentist_id = dentist,
                schedule_id = schedule
            )

            messages.success(request, "Added appointment for " + name + " successfully.")
            return HttpResponseRedirect("/appointment/all/")

    return render(request, "dashboard/add_unregistered_appointment.html",{});


#get a dentists appointment
@csrf_exempt
@login_required
def dentist_schedule_list(request):
    if request.is_ajax():
        print(request.POST)
        day = request.POST.get('day')
        branch = request.POST.get('branch')
        queryset = list(request.user.schedule.filter(Q(weekday=day)|Q(weekday='All'),branch_name=branch).values('id', 'start', 'end','weekday'))
        if len(queryset) == 0:
            return JsonResponse({"message":"No Schedule Available For the Selected Date"}, status=404)
        return JsonResponse({'data': queryset})



@login_required
def edit_appointment(request, id):
    appointment = None

    try:
        appointment = Appointment.objects.prefetch_related().get(dentist=request.user, id=int(id))

    except:
        messages.error(request, "You are not authorized to access the appointment or it doesn't exist")
        return HttpResponseRedirect("/appointment/today/")
    
    if request.method == "POST":
        #print(request.POST)
        appointment.status = request.POST.get('status')

        if int(request.POST.get('schedule')) != appointment.schedule_id:
            appointment.schedule_id = int(request.POST.get('schedule'))
            appointment.status= "pending"

        if request.POST.get('date')!='':
            appointment.date = datetime.datetime.strptime(request.POST.get('date'), "%m/%d/%Y").date()
            appointment.status = "pending"

        appointment.save()
        messages.success(request, "Successfully edited appointment id: " + str(id))
        return HttpResponseRedirect("/appointment/edit/" + str(id)+"/")

    return render(request, "dashboard/appointment_edit.html", {'appointment': appointment, 'patient': appointment.patient, 'schedule': appointment.schedule, 'schedules': appointment.dentist.schedule.all()})