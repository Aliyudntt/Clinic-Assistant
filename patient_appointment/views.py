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


from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from authentication.models import AuthUser
from authentication.models import Schedule


from .models import Patient
from .models import Appointment

# Create your views here.
@csrf_exempt
def schedule_appointment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        email = request.POST.get('email',"")
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number').replace(' ', '').replace('-', '')
        date = datetime.datetime.strptime(request.POST.get('date'), "%m/%d/%Y").date()
        dentist = int(request.POST.get('dentist'))
        schedule = int(request.POST.get('schedule'))
        
        
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
def dentist_schedules(request: HttpRequest):
    if  request.is_ajax():
        day = request.POST.get('day')
        branch = request.POST.get('branch')

        dentists = AuthUser.objects.filter(
            schedule__weekday=day,
            schedule__branch_name=branch,
            is_active=True,
            is_admin=False
        ).prefetch_related('schedule')

        if not dentists:
            return JsonResponse({'message': 'Sorry, no dentist is available'}, status=404)

        dentist_list = []
        for dentist in dentists:
            schedules = Schedule.objects.filter(
                Q(dentist=dentist),
                Q(weekday=day) | Q(weekday='All'),
                branch_name=branch
            ).values('id', 'start', 'end', 'weekday')

            dentist_data = {
                'id': dentist.id,
                'name': dentist.get_full_name(),
                'schedules': list(schedules)
            }

            dentist_list.append(dentist_data)

        return JsonResponse({'data': dentist_list})

    return JsonResponse({'message': 'Invalid request'}, status=400)

#list appointments of a doctors
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


#create unregistered appointment on the fly by doctor
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


#get a doctors appointment
@csrf_exempt
@login_required
def dentist_schedule_list(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print(request.POST)
        day = request.POST.get('day')
        branch = request.POST.get('branch')
        queryset = list(request.user.schedule.filter(Q(weekday=day) | Q(weekday='All'), branch_name=branch).values('id', 'start', 'end', 'weekday'))
        if len(queryset) == 0:
            return JsonResponse({"message": "No Schedule Available For the Selected Date"}, status=404)
        return JsonResponse({'data': queryset})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)



@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, dentist=request.user, id=id)

    if request.method == "POST":
        appointment.status = request.POST.get('status')

        schedule_id = int(request.POST.get('schedule'))
        if schedule_id != appointment.schedule_id:
            appointment.schedule_id = schedule_id
            appointment.status = "pending"

        date = request.POST.get('date')
        if date:
            appointment.date = timezone.datetime.strptime(date, "%m/%d/%Y").date()
            appointment.status = "pending"

        appointment.save()
        messages.success(request, f"Successfully edited appointment id: {id}")
        return redirect('edit_appointment', id=id)

    schedules = appointment.dentist.schedule.all()
    return render(request, "dashboard/appointment_edit.html", {
        'appointment': appointment,
        'patient': appointment.patient,
        'schedule': appointment.schedule,
        'schedules': schedules
    })