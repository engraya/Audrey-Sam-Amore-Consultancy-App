from django.contrib import admin
from .models import ConsultCategories, UserProfile, ConsultationRequest, ConsultancyService

# Register your models here.

admin.site.register(ConsultCategories)
admin.site.register(UserProfile)
admin.site.register(ConsultationRequest)
admin.site.register(ConsultancyService)