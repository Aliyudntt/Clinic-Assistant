from django.shortcuts import render

from authentication.models import AuthUser

# render the index page
def index(request):
    return render(request, 'mainsite/index.html', {'title': 'CDC | Home',})



def contactUs(request):
    return render(request, 'mainsite/contactUs.html', {'title': 'CDC | Contact Us'})


def dentists(request):
    dentists = AuthUser.objects.prefetch_related().filter(is_admin=False)
    return render(request, 'mainsite/dentist.html', {'title':'CDC | Dentists', 'dentists':dentists})


def diagnosis(request):
    return render(request, 'mainsite/diagnosis.html',{'title':'CDC | Diagnosis'})

def personal_care(request):
    return render(request,'mainsite/personalCare.html',{'title': 'CDC | Personal Care'})

def services(request):
    return render(request,'mainsite/services.html',{"title": 'CDC | Services'})


def news(request):
    return render(request, 'mainsite/news.html',{'title': 'CDC | News'})


def treatment(request):
    return render(request, 'mainsite/treatment.html',{'title': "CDC | Treatment"})


def gallary(request):
    return render(request, 'mainsite/gallary.html', {'title':'CDC | Gallery'})