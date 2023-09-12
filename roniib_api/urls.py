from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

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
]
