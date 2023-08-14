from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.homePage, name='home'),
    path('signUp', views.signUp, name='register'),
    path('signIn', views.signIn, name='login'),
    path('signOut', views.signOut, name='logout'),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('services', views.services, name="services"),

    path('profile/<str:username>', views.profile, name="profile"),
    path("consultant/<str:username>/services", views.consultantServices, name="consultant_sevices"),
    path('service/<int:serviceID>', views.consultancyServiceDetail, name="service_detail"),
    path('consultation/requests', views.consultationRequest, name="consultation_request"),
    path('consultation/requests/<int:requestID>/<str:action>/', views.acceptDeclineRequest, name="accept_decline_request"),



    path('notifications', views.notiifcations, name='notifications'),
    path('messaging/<str:recipientUsername>/', views.messaging, name='messaging'),
    path('send_message/', views.sendMessage, name='sendMessage'),
    path('get_notifications_message_count/', views.notificationsMessageCount, name='get_notifications_message_count'),
    path('loadMessages/<str:recipient_username>/', views.loadMessages, name='loadMessages'),




    
    #password Reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="network/passwordManage/password_reset_form.html"), name="reset_password"),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="network/passwordManage/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="network/passwordManage/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="network/passwordManage/password_reset_complete.html"), name="password_reset_complete")
]

