from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('reset_pass/', views.reset_password, name='reset_pass'),
    path('reset_pass_code/', views.reset_password_code, name='reset_pass_code'),
    path('resend_ver_code/', views.resendResetCode, name='resend_ver_code'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('terms/', views.terms_conditions, name='terms'),
    path('myaccount/', views.myAccount, name='myaccount'),
    path('documentation/', views.documentation, name='documentation'),
    path('categories/', views.apicategories, name='apicategories'),
    path('verify/', views.verificationPage, name='verify'),
    path('req_verify/', views.request_ver_link, name='req_verify'),
    path('changeemail/', views.change_email, name='change_email'),
    path('generateNewToken/', views.generateNewToken, name='generateNewToken'),

    path('payment_successful/', views.payment_successful, name='payment_successful'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('paypal_notification/', views.paypal_notification, name='paypal_notification'),

    path('paypal/', include("paypal.standard.ipn.urls")),

    # path('paypal_notification/', views.Privacy_Policy, name='paypal_notification'),

]
