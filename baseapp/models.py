from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from PIL import Image
from datetime import datetime

# Create your models here.

class ConsultCategories(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='media')

    def __str__(self):
        return self.title


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('consultant', 'Consultant')
    )
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=12, null=True, blank=True, choices=GENDER_CHOICES)
    profession = models.CharField(max_length=100, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    profilePicture = models.ImageField(upload_to='profilePics/', blank=True, null=True)
    userType = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username



class ConsultancyService(models.Model):
    title = models.CharField(max_length=200)
    serviceDescripton = models.TextField()
    serviceRate = models.DecimalField(max_digits=10, decimal_places=2)
    consultant = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.CharField(max_length=100)
    serviceCaption = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title


class ConsultationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Consultation_consultant')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Consultation_client')
    service = models.ForeignKey(ConsultancyService, on_delete=models.CASCADE)
    requestMesssage = models.TextField()
    requestStatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)



class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='Appointment_client')
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Appointment_consultant')
    appointment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()



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


class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultant')
    expertise = models.CharField(max_length=100)
    bio = models.TextField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    contact_info = models.CharField(max_length=200)


#.............................New Models.....................#####



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Consultant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=40,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=40,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=False)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=False)
    doctorId=models.PositiveIntegerField(null=False)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=False)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=40,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

class Patient_presscription(models.Model):
    patientId=models.PositiveIntegerField(null=False)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=40,null=True)
    symptoms = models.CharField(max_length=100,null=True)
    presscription = models.TextField(max_length=100,null=True, blank=True)
    presscription1 = models.TextField(max_length=100,null=True, blank=True)


    


