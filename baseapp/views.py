from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import ConsultCategories, UserProfile, ConsultancyService, ConsultancyRequest
# Create your views here.


def homePage(request):
    categories = ConsultCategories.objects.all()
    context = {'categories' : categories}
    return render(request, 'baseapp/homePage.html', context)


def signUp(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registration Succesful...")
            return redirect("home")
        else:
            messages.error(request, "Registration Unsuccessful, Invalid Credentials Entered!!")
    else:
        form = UserRegistrationForm()

    context = {'form' : form}
    return render(request, 'baseapp/registerPage.html', context)


def signIn(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Congratulations, you are now logged in....")
                return redirect("home")
            else:
                messages.error(request, "Invalid Credentials Entered..Try again Later!!")

        else:
            messages.error(request, "Invalid Username or Password used....Try again Later!!!")
    else:
        form = UserLoginForm()
    context = {'form' : form}
    return render(request, 'baseapp/loginPage.html', context)

      
def signOut(request):
    logout(request)
    messages.info(request, "Successfully Logged out!!")
    return redirect("login")


def contact(request):
    context = {}
    return render(request, 'baseapp/contactPage.html', context)


def about(request):
    context = {}
    return render(request, 'baseapp/aboutPage.html', context)



def services(request):
    context = {}
    return render(request, 'baseapp/servicesPage.html', context)


def Profile(request, username):
    userProfile = get_object_or_404(UserProfile, userUsername=username)
    context = {'userProfile' : userProfile}
    return render(request, 'baseapp/userProfile.html', context)


def ConsultantServices(request, username):
    services = ConsultancyService.objects.filter(consultantUsername=username)
    context = {'services' : services}
    return render(request, 'baseapp/consultantServices.html', context)


def ConsultancyServiceDetail(request, serviceID):
    service = get_object_or_404(ConsultancyService, id=serviceID)
    if request.method == 'POST':
        ConsultancyRequest.objects.create(
            client=request.user,
            consultant=service.consultant,
            service=service
        )
        return redirect('userProfile', username=request.user.username)
    context = {'service' : service}
    return render(request, 'baseapp/serviceDetail.html', context)

def consultationRequest(request):
    consultationRequests = ConsultancyRequest.objects.filter(consultant=request.user)
    context = {'consultationRequests' : consultationRequests}
    return render(request, 'baseapp/consultationRequest.html', context)


def acceptOrDeclineRequest(request, request.id, action):
    consultationRequest = get_object_or_404(ConsultancyRequest, id=request.id)
    if action == 'Accept':
        consultationRequest.requestStatus = 'Accepted'
        consultationRequest.save()
    elif action == 'Decline':
        consultationRequest.requestStatus = 'Declined'
        consultationRequest.save()
    return redirect('consultationRequests')
