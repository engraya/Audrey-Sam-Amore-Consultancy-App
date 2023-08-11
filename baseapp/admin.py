from django.contrib import admin
from .models import ConsultCategories, Profile, ConsultationRequest, ConsultancyService, Notification, Message

# Register your models here.

admin.site.register(ConsultCategories)
admin.site.register(Profile)
admin.site.register(ConsultationRequest)
admin.site.register(ConsultancyService)
admin.site.register(Notification)
admin.site.register(Message)