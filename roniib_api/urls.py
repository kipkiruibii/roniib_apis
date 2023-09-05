from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('register/',views.register,name='register'),
    path('contact/',views.contact,name='contact'),
    path('pricing/',views.pricing,name='pricing'),
    path('browse/',views.browse,name='browse'),
    path('terms/',views.terms_conditions,name='terms'),

    #categories
    path('all/', views.all, name='all'),
    path('sports/', views.sports, name='sports'),
    path('entertainment/', views.entertainment, name='entertainment'),
    path('finance/', views.finance, name='finance'),
    path('weather/', views.weather, name='weather'),
    path('text/', views.text, name='text'),
    path('lexical/', views.lexical, name='lexical'),
    path('tools/', views.tools, name='tools'),
    path('music/', views.music, name='music'),
    path('food/', views.food, name='food'),
    path('education/', views.education, name='education'),
    path('health/', views.health, name='health'),
    path('myaccount/', views.myAccount, name='myaccount'),

    #documentation
    path('documentation/', views.documentation, name='documentation'),



]
