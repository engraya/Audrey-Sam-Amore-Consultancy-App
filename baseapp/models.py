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
    country = CountryField(blank_label="Select Country")
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
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultant')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    service = models.ForeignKey(ConsultancyService, on_delete=models.CASCADE)
    requestMesssage = models.TextField()
    requestStatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_messages')
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


    





