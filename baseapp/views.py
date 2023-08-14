from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import ConsultCategories, Profile, ConsultancyService, ConsultationRequest, Notification, Message, User
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


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {'profile' : profile}
    return render(request, 'baseapp/userProfile.html', context)




def consultantServices(request, username):
    services = ConsultancyService.objects.filter(consultant__username=username)
    context = {'services': services}
    return render(request, 'baseapp/consultantServices.html', context)




def consultancyServiceDetail(request, serviceID):
    service = get_object_or_404(ConsultancyService, id=serviceID)
    if request.method == 'POST':
        ConsultationRequest.objects.create(
            client=request.user,
            consultant=service.consultant,
            service=service
        )
        return redirect('profile', username=request.user.username)
    context = {'service' : service}
    return render(request, 'baseapp/serviceDetail.html', context)



def consultationRequest(request):
    consultationRequests = ConsultationRequest.objects.filter(consultant=request.user)
    context = {'consultationRequests' : consultationRequests}
    return render(request, 'baseapp/consultationRequests.html', context)



def acceptDeclineRequest(request, requestID, action):
    consultationRequest = get_object_or_404(ConsultationRequest, id=requestID)
    if action == 'accept':
        consultationRequest.requestStatus = 'accepted'
        consultationRequest.save()
    elif action == 'decline':
        consultationRequest.requestStatus = 'declined'
        consultationRequest.save()
    return redirect('consultation_request')



def notiifcations(request):
    user = request.user
    notifcations = Notification.objects.filter(user=user)
    context = {'notifications' : notifcations}
    return render(request, 'baseapp/notifications.html', context)




def messaging(request, recipientUsername):
    sender = request.user
    recipient = get_object_or_404(User, username=recipientUsername)

    if request.method == 'POST':
        messageContent = request.POST.get('messageContent')
        Message.objects.create(sender=sender, recipient=recipient, messageContent=messageContent)
        return redirect('messaging', recipientUsername=recipientUsername)
    

    messages = Message.objects.filter(sender=sender, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=sender)
    messages = messages.order_by('timestamp')

    context = {'recipient' : recipient, 'messages' : messages}
    return render(request, 'baseapp/messaging.html', context)




def sendMessage(request):
    if request.method == 'POST':
        sender = request.user
        recipientusername = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipientusername)
        messageContent = request.POST.get('messageContent')
        Message.objects.create(sender=sender, recipient=recipient, messageContent=messageContent)
        return JsonResponse({'success' : True})
    return JsonResponse({'success' : False})
    


def notificationsMessageCount(request):
    user = request.user
    notiifcationCount = Notification.objects.filter(user=user, read=False).count()
    messageCount = Message.objects.filter(recipient=user).count()

    return JsonResponse({
        'notification_count' : notiifcationCount,
        'message_count' : messageCount
    })


def loadMessages(request, recipient_username):
    sender = request.user
    recipient = User.objects.get(username=recipient_username)
    messages = Message.objects.filter(
        (models.Q(sender=sender) & models.Q(recipient=recipient)) | 
        (models.Q(sender=recipient) & models.Q(recipient=sender))
    )

    messages_data = [{'content' : message.messsageContent, 'sender' : message.sender.username} for message in messages]
    return JsonResponse({'messages' : messages_data})










