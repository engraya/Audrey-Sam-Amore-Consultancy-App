from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import AdminRegistrationForm, UserLoginForm, AppointmentForm, AppointmentRequestForm, AppointmentResponseForm, MessageForm
from django.contrib.auth.decorators import login_required
from .models import *
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date



# Create your views here.


#BASE PRELOGIN VIEWS
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'baseapp/homePage.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'baseapp/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def consultantclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'baseapp/consultantclick.html')


#for showing signup/login button for patient(by sumit)
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'baseapp/clientclick.html')


#-------------Registration Views--------#
def admin_signup_view(request):
    form=forms.AdminRegistrationForm()
    context = {'form': form}
    if request.method=='POST':
        form=forms.AdminRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'baseapp/adminsignup.html', context)




def consultant_signup_view(request):
    userForm=forms.ConsultantUserForm()
    context = {'userForm':userForm}
    if request.method=='POST':
        userForm=forms.ConsultantUserForm(request.POST)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            my_consultant_group = Group.objects.get_or_create(name='CONSULTANT')
            my_consultant_group[0].user_set.add(user)
        return HttpResponseRedirect('consultantlogin')
    return render(request,'baseapp/consultantsignup.html', context)



def client_signup_view(request):
    userForm=forms.ClientUserForm()
    context = {'userForm' : userForm}
    if request.method=='POST':
        userForm = forms.ClientUserForm(request.POST)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('clientlogin')
    return render(request,'baseapp/clientsignup.html', context)





#-----------for checking user is CONSULTANT , CLIENT or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_consultant(user):
    return user.groups.filter(name='CONSULTANT').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CONSULTANT OR CLIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_consultant(request.user):
        accountapproval=models.Consultant.objects.all().filter(user_id=request.user.id,availability_status=True)
        if accountapproval:
            return redirect('consultant-dashboard')
        else:
            return render(request,'baseapp/consultant_wait_for_approval.html')
    elif is_client(request.user):
        accountapproval=models.Client.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('client-dashboard')
        else:
            return render(request,'baseapp/client_wait_for_approval.html')



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def admin_dashboard_view(request):
    #for both table in admin dashboard
    # consultants=models.Consultant.objects.all().order_by('-id')
    # clients=models.Client.objects.all().order_by('-id')
    # #for three cards
    # consultantcount=models.Consultant.objects.all().filter(status=True).count()
    # pendingconsultantcount=models.Consultant.objects.all().filter(status=False).count()

    # patientcount=models.Client.objects.all().filter(status=True).count()
    # pendingclientcount=models.Client.objects.all().filter(status=False).count()

    # appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    # pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    # mydict={
    # 'doctors':doctors,
    # 'patients':patients,
    # 'doctorcount':doctorcount,
    # 'pendingdoctorcount':pendingdoctorcount,
    # 'patientcount':patientcount,
    # 'pendingpatientcount':pendingpatientcount,
    # 'appointmentcount':appointmentcount,
    # 'pendingappointmentcount':pendingappointmentcount,
    # }
    return render(request,'baseapp/admin_dashboard.html')





#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def consultant_dashboard_view(request):
    #for three cards
    # patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    # appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    # patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    # #for  table in doctor dashboard
    # appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    # patientid=[]
    # for a in appointments:
    #     patientid.append(a.patientId)
    # patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    # appointments=zip(appointments,patients)
    # mydict={
    # 'patientcount':patientcount,
    # 'appointmentcount':appointmentcount,
    # 'patientdischarged':patientdischarged,
    # 'appointments':appointments,
    # 'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    # }
    return render(request,'baseapp/consultant_dashboard.html',)













#---------------------------------------------------------------------------------
#------------------------ CLIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def client_dashboard_view(request):
    # patient=models.Patient.objects.get(user_id=request.user.id)
    # doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    # mydict={
    # 'patient':patient,
    # 'doctorName':doctor.get_name,
    # 'doctorMobile':doctor.mobile,
    # 'doctorAddress':doctor.address,
    # 'symptoms':patient.symptoms,
    # 'doctorDepartment':doctor.department,
    # 'admitDate':patient.admitDate,
    # }
    return render(request,'baseapp/client_dashboard.html')















#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#####
def homePage(request):
    categories = ConsultancyCategories.objects.all()
    context = {'categories' : categories}
    return render(request, 'baseapp/homePage.html', context)


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


def consultantsList(request):
    consultants = Consultant.objects.all()
    context = {'consultants' : consultants}
    return render(request, 'baseapp/consultants_list.html', context)


def consultant_detail(request, consultant_id):
    consultant = get_object_or_404(Consultant, id=consultant_id)
    context = {'consultant' : consultant}
    return render(request, 'baseapp/consultant_detail.html', context)


def scheduleAppointment(request, consultant_id):
    consultant = get_object_or_404(Consultant, id=consultant_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.consultant = consultant
            appointment.save()

            return redirect('appointment_confirmation')
    else:
        form = AppointmentForm()
    context = {'form' : form, 'consultant' : consultant}
    return render(request, 'baseapp/schedule_appointment.html', context)


def manageAppointments(request):
    appointments = Appointment.objects.filter(client=request.user.client)
    context = {'appiontments' : appointments}
    return render(request, 'baseapp/manage_appiontments.html', context)


def cancelAppointment(request, appointment_id):
    appiontment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.client == appiontment.client:
        appiontment.delete()

    return redirect('manage_appiontments')


def clientDashboard(request):
    client = request.user.client
    appiontments = Appointment.objects.filter(client=client)
    context = {'client' : client, 'appointments' : appiontments}
    return render(request, 'baseapp/client_dashboard.html', context)


def sendMessage(request, reciever_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        reciever = User.objects.get(id=reciever_id)
        message = Message.objects.create(sender=request.user, reciever=reciever, content=content)
        message.save()

        notification = Notification.objects.create(user=reciever, message=f'You have a New Message from {request.user}')
        notification.save()

        return redirect('inbox')



def inbox(request):
    recieved_messages = Message.objects.filter(reciever=request.user)
    context = {'messages' : recieved_messages}
    return render(request, 'baseapp/inbox.html', context)



def notifications(request):
    notifcations =Notification.objects.filter(user=request.user).order_by('-timestamp')
    context = {'notifications' : notifcations}
    return render(request, 'baseapp/notifications.html', context)


def mark_notifications_as_read(request, notifcation_id):
    try:
        notification = Notification.objects.get(id=notifcation_id, user=request.user)
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return JsonResponse({'status' : 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status' : 'error'}, status=404)


def request_appointment(request, consultant_id):
    consultant = User.objects.get(id=consultant_id)
    
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            # Your appointment request logic here...
            
            # Create a notification for the consultant
            message = f"A client has requested an appointment with you."
            notification = Notification(user=consultant, message=message)
            notification.save()
            
            return redirect('appointment_request_confirmation')  # Redirect to a confirmation page
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'consultancy/request_appointment.html', {'form': form, 'consultant': consultant})



def respond_appointment_request(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    client = appointment.client
    
    if request.method == 'POST':
        form = AppointmentResponseForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            
            # Update the appointment status
            appointment.status = response
            appointment.save()
            
            # Create a notification for the client
            message = f"Your appointment request has been {response}."
            notification = Notification(user=client, message=message)
            notification.save()
            
            return redirect('appointment_response_confirmation')  # Redirect to a confirmation page
    else:
        form = AppointmentResponseForm()
    
    return render(request, 'consultancy/respond_appointment_request.html', {'form': form, 'appointment': appointment})



def respond_to_client(request, client_id):
    client = User.objects.get(id=client_id)
    
    if request.method == 'POST':
        response_message = request.POST['response_message']  # Adjust this based on your form
        # Your response logic here...

        # Create a notification for the client
        message = f"A response has been received from the consultant: {response_message}"
        notification = Notification(user=client, message=message)
        notification.save()

        return redirect('response_confirmation')  # Redirect to a confirmation page

    return render(request, 'consultancy/respond_to_client.html', {'client': client})



def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            
            # Create a notification for the recipient
            notification = Notification(user=recipient, message=message)
            notification.save()
            
            return redirect('message_sent_confirmation')  # Redirect to a confirmation page
    else:
        form = MessageForm()
    
    return render(request, 'consultancy/send_message.html', {'form': form, 'recipient': recipient})


def appointmentConfirmation(request):
    return render(request, 'baseapp/appointment_confirmation.html')


# def mark_notifications_as_read(request, notiifcation_id):
#     notification = Notification.objects.get(id=notiifcation_id)
#     notification.is_read = True
#     notification.save()
#     return redirect('notifications')

# def notiifcations(request):
#     user = request.user
#     notifcations = Notification.objects.filter(user=user)
#     context = {'notifications' : notifcations}
#     return render(request, 'baseapp/notifications.html', context)


# def notificationsMessageCount(request):
#     user = request.user
#     notiifcationCount = Notification.objects.filter(user=user, read=False).count()
#     messageCount = Message.objects.filter(recipient=user).count()

#     return JsonResponse({
#         'notification_count' : notiifcationCount,
#         'message_count' : messageCount
#     })


# def loadMessages(request, recipient_username):
#     sender = request.user
#     recipient = User.objects.get(username=recipient_username)
#     messages = Message.objects.filter(
#         (models.Q(sender=sender) & models.Q(recipient=recipient)) | 
#         (models.Q(sender=recipient) & models.Q(recipient=sender))
#     )

#     messages_data = [{'content' : message.messsageContent, 'sender' : message.sender.username} for message in messages]
#     return JsonResponse({'messages' : messages_data})



# def messaging(request, recipientUsername):
#     sender = request.user
#     recipient = get_object_or_404(User, username=recipientUsername)
#     if request.method == 'POST':
#         messageContent = request.POST.get('messageContent')
#         Message.objects.create(sender=sender, recipient=recipient, messageContent=messageContent)
#         return redirect('messaging', recipientUsername=recipientUsername)
#     messages = Message.objects.filter(sender=sender, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=sender)
#     messages = messages.order_by('timestamp')

#     context = {'recipient' : recipient, 'messages' : messages}
#     return render(request, 'baseapp/messaging.html', context)


# def sendMessage(request):
#     if request.method == 'POST':
#         sender = request.user
#         recipientusername = request.POST.get('recipient')
#         recipient = get_object_or_404(User, username=recipientusername)
#         messageContent = request.POST.get('messageContent')
#         Message.objects.create(sender=sender, recipient=recipient, messageContent=messageContent)
#         return JsonResponse({'success' : True})
#     return JsonResponse({'success' : False})




    









