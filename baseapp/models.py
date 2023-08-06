from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ConsultCategories(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='media')

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('Client', 'Client'),
        ('Consultant', 'Consultant')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    profilePicture = models.ImageField(upload_to='profilePics/', blank=True, null=True)
    userType = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    specialization = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user


class ConsultancService(models.Model):
    title = models.CharField(max_length=200)
    serviceDescripton = models.TextField()
    serviceRate = models.DecimalField(max_digits=10, decimal_places=2)
    consultant = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ConsultancyRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined')
    )
    consultant = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(ConsultancService, on_delete=models.CASCADE)
    requestStatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')



