from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Consultant, Client, Appointment



# ADMIN REGISTRATION FORM
class AdminRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your First Name'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Last Name'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Email'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Confirm your Password'})

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


#Consultant related form
class ConsultantUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class ConsultantForm(forms.ModelForm):
    class Meta:
        model= Consultant
        fields=['address','mobile','consultantcyServiceSpeciality','availability_status','profilePicture']

#Client User Form
class ClientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class ClientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedConsultantID=forms.ModelChoiceField(queryset=Consultant.objects.all().filter(availability_status=True),empty_label="Name and Service Speciality", to_field_name="user_id")
    class Meta:
        model= Client
        fields=['address','mobile','profilePicture']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})
        
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    consultantID=forms.ModelChoiceField(queryset=Consultant.objects.all().filter(availability_status=True),empty_label="Name and Service Speciality", to_field_name="user_id")
    clientID=forms.ModelChoiceField(queryset=Client.objects.all().filter(status=True),empty_label="Patient Name", to_field_name="user_id")
    class Meta:
        model = Appointment
        fields = ['notes','description','status']


#for CONTACT US page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class AppointmentRequestForm(forms.Form):
    appointment_date = forms.DateTimeField(label='Appointment Date and Time', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    notes = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'rows': 4}))

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        # Add validation logic here if needed
        # For example, ensure the appointment date is in the future
        return appointment_date


class AppointmentResponseForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['notes']

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))


