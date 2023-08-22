from django.contrib import admin
from .models import ConsultCategories, Profile, Client, Consultant, ConsultationRequest, ConsultancyService, Notification, Message, Appointment

# Register your models here.

admin.site.register(ConsultCategories)
admin.site.register(Profile)
admin.site.register(ConsultationRequest)
admin.site.register(ConsultancyService)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Client)
admin.site.register(Consultant)
admin.site.register(Appointment)