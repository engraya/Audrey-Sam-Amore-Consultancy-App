from django.contrib import admin
from .models import ConsultCategories, Client, Consultant, ConsultationRequest, ConsultancyService, Notification, Message, Appointment
from .models import Profile
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




#..........................New Registers...................#

from .models import Doctor,Patient,Appointment,PatientDischargeDetails, Patient_presscription
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
admin.site.register(Patient_presscription)