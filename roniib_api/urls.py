from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('register/',views.register,name='register'),
    path('contact/',views.contact,name='contact'),
    path('pricing/',views.pricing,name='pricing'),
    path('terms/',views.terms_conditions,name='terms'),
    path('myaccount/', views.myAccount, name='myaccount'),
    path('documentation/', views.documentation, name='documentation'),
    path('categories/', views.apicategories, name='apicategories'),
    path('verify/', views.verificationPage, name='verify'),
    path('req_verify/', views.request_ver_link, name='req_verify'),
    path('changeemail/', views.change_email, name='change_email'),
]
