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


#---------------------------------BASE PRELOGIN VIEWS--------------------------#
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
    # for both table in admin dashboard
    consultants=models.Consultant.objects.all().order_by('-id')
    clients=models.Client.objects.all().order_by('-id')
    #for three cards
    consultantcount=models.Consultant.objects.all().filter(status=True).count()
    pendingconsultantcount=models.Consultant.objects.all().filter(status=False).count()

    clientcount=models.Client.objects.all().filter(status=True).count()
    pendingclientcount=models.Client.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    context = {
    'consultants':consultants,
    'clients':clients,
    'consultantcount':consultantcount,
    'pendingconsultantcount':pendingconsultantcount,
    'clientcount':clientcount,
    'pendingclientcount':pendingclientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'baseapp/admin_dashboard.html', context)


# this view for sidebar click on admin page

def admin_consultant_view(request):
    return render(request,'baseapp/admin_consultant.html')




def admin_view_consultant_view(request):
    consultants = models.Consultant.objects.all().filter(status=True)
    context = {'consultants':consultants}
    return render(request,'baseapp/admin_view_consultant.html', context)




def delete_consultant_from_hospital_view(request,pk):
    consultant=models.Consultant.objects.get(id=pk)
    user=models.User.objects.get(id=consultant.user_id)
    user.delete()
    consultant.delete()
    return redirect('admin-view-consultant')




def update_doctor_view(request,pk):
    consultant=models.Consultant.objects.get(id=pk)
    user=models.User.objects.get(id=consultant.user_id)

    userForm=forms.ConsultantUserForm(instance=user)
    consultantForm=forms.ConsultantForm(request.FILES,instance=consultant)
    context = {'userForm':userForm,'consultantForm':consultantForm}
    if request.method=='POST':
        userForm=forms.ConsultantUserForm(request.POST,instance=user)
        consultantForm=forms.ConsultantForm(request.POST,request.FILES,instance=consultant)
        if userForm.is_valid() and consultantForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            consultant=consultantForm.save(commit=False)
            consultant.status=True
            consultant.save()
            return redirect('admin-view-consultant')
    return render(request,'baseapp/admin_update_consultant.html',context)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_consultant_view(request):
    userForm=forms.ConsultantUserForm()
    consultantForm=forms.ConsultantForm()
    context = {'userForm':userForm,'consultantForm':consultantForm}
    if request.method=='POST':
        userForm=forms.ConsultantUserForm(request.POST)
        consultantForm=forms.ConsultantForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            consultant=consultantForm.save(commit=False)
            consultant.user=user
            consultant.status=True
            consultant.save()

            my_consultant_group = Group.objects.get_or_create(name='CONSULTANT')
            my_consultant_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-consultant')
    return render(request,'baseapp/admin_add_consultant.html',context)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_consultant_view(request):
    #those whose approval are needed
    consultant = models.Consultant.objects.all().filter(status=False)
    context = {'consultant':consultant}
    return render(request,'baseapp/admin_approve_consultant.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_consultant_view(request,pk):
    consultant = models.Consultant.objects.get(id=pk)
    consultant.status=True
    consultant.save()
    return redirect(reverse('admin-approve-consultant'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_consultant_view(request,pk):
    consultant = models.Consultant.objects.get(id=pk)
    user=models.User.objects.get(id=consultant.user_id)
    user.delete()
    consultant.delete()
    return redirect('admin-approve-consultant')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_consultant_specialisation_view(request):
    consultant = models.Consultant.objects.all().filter(status=True)
    context = {'consultant':consultant}
    return render(request,'baseapp/admin_view_consultant_specialisation.html', context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_client_view(request):
    return render(request,'baseapp/admin_client.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_client_view(request):
    clients = models.Patient.objects.all().filter(status=True)
    context = {'clients':clients}
    return render(request,'baseapp/admin_view_patient.html', context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_client_from_hospital_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_client_view(request,pk):
    cleint=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)

    userForm=forms.ClientUserForm(instance=user)
    clientForm=forms.ClientForm(request.FILES,instance=client)
    context = {'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST,instance=user)
        clientForm=forms.ClientForm(request.POST,request.FILES,instance=client)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.status=True
            client.assignedConsultantID=request.POST.get('assignedConsultantID')
            client.save()
            return redirect('admin-view-client')
    return render(request,'baseapp/admin_update_client.html', context)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_client_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    context = {'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            client=clientForm.save(commit=False)
            client.user=user
            client.status=True
            client.assignedConsultantID=request.POST.get('assignedConsultantID')
            client.save()

            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-client')
    return render(request,'baseapp/admin_add_client.html',context)




#------------------FOR APPROVING CLIENTS BY ADMIN----------------------

def admin_approve_client_view(request):
    #those whose approval are needed
    clients = models.Client.objects.all().filter(status=False)
    context = {'clients':clients}
    return render(request,'baseapp/admin_approve_client.html', context)



def approve_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    client.status=True
    client.save()
    return redirect(reverse('admin-approve-client'))



def reject_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-approve-client')


#-----------------APPOINTMENT START----------------------------------------------------------------#####

def admin_appointment_view(request):
    return render(request,'baseapp/admin_appointment.html')



def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    context = {'appointments':appointments}
    return render(request,'baseapp/admin_view_appointment.html', context)



def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    context = {'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.consultantID=request.POST.get('consultantID')
            appointment.clientID=request.POST.get('clientID')
            appointment.appointmentRequestCategory=request.POST.get('category')
            appointment.description=request.POST.get('description')
            appointment.notes=request.POST.get('notes')
            appointment.consultantName=models.User.objects.get(id=request.POST.get('consultantID')).first_name
            appointment.clientName=models.User.objects.get(id=request.POST.get('clientID')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context)



def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    context = {'appointments':appointments}
    return render(request,'baseapp/admin_approve_appointment.html', context)




def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))




def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ CONSULTANT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def consultant_dashboard_view(request):
    # for three cards
    clientcount=models.Client.objects.all().filter(status=True,assignedConsultantID=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id).count()
    clientdischarged=models.ClientDischargeDetails.objects.all().distinct().filter(assignedConsultantName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id).order_by('-id')
    clientID=[]
    for a in appointments:
        clientID.append(a.clientID)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientID).order_by('-id')
    appointments=zip(appointments,clients)
    context = {
    'clientcount':clientcount,
    'appointmentcount':appointmentcount,
    'clientdischarged':clientdischarged,
    'appointments':appointments,
    'consultant':models.Consultant.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'baseapp/consultant_dashboard.html', context)




@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def consultant_client_view(request):
    context = {
    'consultant':models.Consultant.objects.get(user_id=request.user.id), #for profile picture of CONSULTANT in sidebar
    }
    return render(request,'baseapp/doctor_client.html',context)



@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def consultant_view_client_view(request):
    clients = models.Client.objects.all().filter(status=True,assignedConsultantID=request.user.id)
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    context = {'clients':clients,'consultant':consultant}
    return render(request,'baseapp/consultant_view_client.html', context)



@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def consultant_view_discharge_client_view(request):
    dischargedclients = models.ClientDischargeDetails.objects.all().distinct().filter(assignedConsultantName=request.user.first_name)
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of cosultant in sidebar
    context = {'dischargedclients':dischargedclients,'consultant':consultant}
    return render(request,'baseapp/consultant_view_discharge_client.html', context)



@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def consultant_appointment_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of COSULTANT in sidebar
    context = {'consultant':consultant}
    return render(request,'baseapp/consultant_appointment.html', context)



@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def consultant_view_appointment_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id)
    clientID=[]
    for a in appointments:
        clientID.append(a.clientID)
    clients=models.Patient.objects.all().filter(status=True,user_id__in=clientID)
    appointments=zip(appointments, clients)
    context = {'appointments':appointments,'consultant':consultant}
    return render(request,'hospital/doctor_view_appointment.html', context)



@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def consultant_delete_appointment_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    clientID=[]
    for a in appointments:
        clientID.append(a.clientID)
    clients = models.Client.objects.all().filter(status=True,user_id__in=clientID)
    appointments=zip(appointments, clients)
    context = {'appointments':appointments,'consultant':consultant}
    return render(request,'baseapp/consultant_delete_appointment.html', context)



@login_required(login_url='consultantlogin')
@user_passes_test(is_consultant)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id)
    clientID=[]
    for a in appointments:
        clientID.append(a.clientID)
    clients = models.Client.objects.all().filter(status=True,user_id__in=clientID)
    appointments=zip(appointments, clients)
    context = {'appointments':appointments,'consultant':consultant}
    return render(request,'baseapp/consultant_delete_appointment.html', context)



#---------------------------------------------------------------------------------
#------------------------ CONSULTANT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------




#---------------------------------------------------------------------------------
#------------------------ CLIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_dashboard_view(request):
    client = models.Client.objects.get(user_id=request.user.id)
    consultant = models.Consultant.objects.get(user_id=client.assignedConsultantID)
    context = {'client': client,'consultantName': consultant.get_name}
    return render(request,'baseapp/client_dashboard.html',context)



@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_appointment_view(request):
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    context = {'client':client}
    return render(request,'baseapp/client_appointment.html', context)



@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_book_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    context = {'appointmentForm':appointmentForm,'client': client}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.consultantID=request.POST.get('consultantID')
            appointment.cientID=request.user.id #----user can choose any client but only their info will be stored
            appointment.consultantName=models.User.objects.get(id=request.POST.get('consultantID')).first_name
            appointment.clientName=request.user.first_name #----user can choose any CLIENT but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('client-view-appointment')
    return render(request,'baseapp/client_book_appointment.html',context)





@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_view_appointment_view(request):
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    appointments=models.Appointment.objects.all().filter(clientID=request.user.id)
    context = {'appointments':appointments,'client':client}
    return render(request,'baseapp/client_view_appointment.html', context)



#------------------------ CLIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------















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




    









