from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from PIL import Image
from datetime import datetime

# Create your models here.


#.............................New Models.....................#####


class ConsultancyCategories(models.Model):
    title = models.CharField(max_length=200)


    def __str__(self):
        return self.title

CONSULTANCY_CATEGORY=[('Dating','Dating'),
('Relationships','Relationships'),
('Breakups','Breakups'),
('Divorce','Divorce'),
('Marriage','Marriage'),
('Family','Family'),
('Business','Business'),
]
GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female")
    )
APPOINTMENT_REQUEST_CATEGORY=[('Dating','Dating'),
('Relationships','Relationships'),
('Breakups','Breakups'),
('Divorce','Divorce'),
('Marriage','Marriage'),
('Family','Family'),
('Business','Business'),
]
class Consultant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='consultant_user')
    profilePicture = models.ImageField(upload_to='profilePics/', blank=True, null=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=12, null=True, blank=True, choices=GENDER_CHOICES)
    consultantcyServiceSpeciality= models.CharField(max_length=50,choices=CONSULTANCY_CATEGORY)
    availability_status=models.BooleanField(default=False)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id




class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='client_user')
    profilePicture = models.ImageField(upload_to='profilePics/', blank=True, null=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    availability_status=models.BooleanField(default=False)
    gender = models.CharField(max_length=12, null=True, blank=True, choices=GENDER_CHOICES)
    siteRegisterDate = models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    assignedConsultantID = models.PositiveIntegerField(null=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id


class ConsultancyService(models.Model):
    title = models.CharField(max_length=200)
    serviceDescripton = models.TextField()
    serviceRate = models.DecimalField(max_digits=10, decimal_places=2)
    consultant = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.CharField(max_length=100)
    serviceCaption = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title


class Appointment(models.Model):
    clientID=models.PositiveIntegerField(null=False)
    consultantID=models.PositiveIntegerField(null=False)
    clientName=models.CharField(max_length=40,null=True)
    consultantName=models.CharField(max_length=40,null=True)
    appointmentRequestCategory = models.CharField(max_length=100, choices=APPOINTMENT_REQUEST_CATEGORY)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.appiontmentRequestCategory

class ConsultationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_consultant')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_client')
    service = models.ForeignKey(ConsultancyService, on_delete=models.CASCADE)
    requestMesssage = models.TextField()
    requestStatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_messages', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.reciever}'
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user} : {self.message}'

class ClientDischargeDetails(models.Model):
    clientId=models.PositiveIntegerField(null=False)
    clientName=models.CharField(max_length=40)
    assignedconsultantName=models.CharField(max_length=40)
    appiontmentRequestCategory = models.CharField(max_length=100, choices=APPIONTMENT_REQUEST_CATEGORY)
    consultationRequestDate=models.DateField(null=False)
    consultationReleaseDate=models.DateField(null=False)
    consultancyFee=models.PositiveIntegerField(null=False)
    consultantFee=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


class ClientPrescription(models.Model):
    clientId=models.PositiveIntegerField(null=False)
    clientName=models.CharField(max_length=40)
    assignedconsultantName=models.CharField(max_length=40)
    appiontmentRequestCategory = models.CharField(max_length=100, choices=APPIONTMENT_REQUEST_CATEGORY)
    presscription = models.TextField(max_length=100,null=True, blank=True)



    


