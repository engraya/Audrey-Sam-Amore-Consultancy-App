from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.homePage, name='home'),
    path('signUp', views.signUp, name='register'),
    path('signIn', views.signIn, name='login'),
    path('signOut', views.signOut, name='logout'),
    # path('contact', views.contact, name="contact"),
    # path('about', views.about, name="about"),
    # path('services', views.services, name="services"),

    path('profile/<str:username>', views.profile, name="profile"),
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



    # path('notifications', views.notiifcations, name='notifications'),
    # path('messaging/<str:recipientUsername>/', views.messaging, name='messaging'),
    # path('send_message/', views.sendMessage, name='sendMessage'),
    # path('get_notifications_message_count/', views.notificationsMessageCount, name='get_notifications_message_count'),
    # path('loadMessages/<str:recipient_username>/', views.loadMessages, name='loadMessages'),




    
    #password Reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="network/passwordManage/password_reset_form.html"), name="reset_password"),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="network/passwordManage/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="network/passwordManage/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="network/passwordManage/password_reset_complete.html"), name="password_reset_complete")
]

