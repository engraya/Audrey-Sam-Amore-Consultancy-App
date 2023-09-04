from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [

    path('',views.home_view,name='home'),

    
    path('profile/<str:username>', views.profile, name="profile"),

        #password Reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="network/passwordManage/password_reset_form.html"), name="reset_password"),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="network/passwordManage/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="network/passwordManage/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="network/passwordManage/password_reset_complete.html"), name="password_reset_complete"),

 

    path("consultant/<str:username>/services", views.consultantServices, name="consultant_sevices"),
    path('service/<int:serviceID>', views.consultancyServiceDetail, name="service_detail"),
    path('consultation/requests', views.consultationRequest, name="consultation_request"),
    path('consultation/requests/<int:requestID>/<str:action>/', views.acceptDeclineRequest, name="accept_decline_request"),



    path('send_message/<int:reciever_id>/', views.sendMessage, name="send_messsage"),
    path('inbox', views.inbox, name="inbox"),
    path('notifications', views.notifications, name="notifications"),
    path('mark_notification/<int:notification_id>/', views.mark_notifications_as_read, name="mark_notification"),


    path('consultants', views.consultantsList, name="consultants"),
    path('consultant/<str:consultant_id>', views.consultant_detail, name="consultant_detail"),


    path('scheduleAppointment/<int:consultant_id>/', views.scheduleAppointment, name="schedule_appointment"),
    path("appointment_confirmation", views.appointmentConfirmation, name="appointment_confirmation"),
    path('appointments/', views.manageAppointments, name="manage_appointments"),
    path('appointment/<int:appoinntment_id>/cancel', views.cancelAppointment, name="cancel_appointment"),
    path('request_appointment/<int:consultant_id>/', views.request_appointment, name='request_appointment'),
    path('respond_appointment_request/<int:appointment_id>/', views.respond_appointment_request, name='respond_appointment_request'),
    path('respond_to_client/<int:client_id>/', views.respond_to_client, name='respond_to_client'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),




    # path('book_appointment/', views.AppointmentTemplateView.as_view(), name='book'),
    # path('manage-appointments/', views.ManageAppointmentTemplateView.as_view(), name='manage'),




    # path('notifications', views.notiifcations, name='notifications'),
    # path('messaging/<str:recipientUsername>/', views.messaging, name='messaging'),
    # path('send_message/', views.sendMessage, name='sendMessage'),
    # path('get_notifications_message_count/', views.notificationsMessageCount, name='get_notifications_message_count'),
    # path('loadMessages/<str:recipient_username>/', views.loadMessages, name='loadMessages'),

    
    path('adminclick', views.adminclick_view),
    path('doctorclick', views.consultantclick_view),
    path('patientclick', views.clientclick_view),


    path('adminsignup', views.admin_signup_view),
    path('consultantsignup', views.consultant_signup_view,name='consultantsignup'),
    path('clientsignup', views.client_signup_view),
    path('adminlogin', LoginView.as_view(template_name='baseapp/adminlogin.html')),
    path('consultantlogin', LoginView.as_view(template_name='baseapp/consultantlogin.html')),
    path('clientlogin', LoginView.as_view(template_name='baseapp/clientlogin.html')),



    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='baseapp/index.html'),name='logout'),

   

]

