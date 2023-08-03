from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
# Create your views here.


def homePage(request):
    context = {}
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