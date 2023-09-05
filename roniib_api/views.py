from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def home(request):
    return render(request,'index.html')
def pricing(request):
    return render(request,'pricing.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    message=''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message='login successful'
            print(message)
            return redirect('home')

        else:

            message='Invalid credentials.'
            print(message)
            return render(request, 'login.html', context={'message': message})

    else:
        return render(request,'login.html',context={'message':message})

def log_out(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request,'register.html')
def contact(request):
    return render(request,'contact.html')
def browse(request):
    return render(request,'browse.html')

#categories
def all(request):
    return render(request,'all.html')
def sports(request):
    return render(request,'sports.html')
def entertainment(request):
    return render(request,'entertainment.html')
def finance(request):
    return render(request,'finance.html')
def weather(request):
    return render(request,'weather.html')
def text(request):
    return render(request,'text.html')
def lexical(request):
    return render(request,'lexical.html')
def tools(request):
    return render(request,'tools.html')
def music(request):
    return render(request,'music.html')
def food(request):
    return render(request,'food.html')
def education(request):
    return render(request,'education.html')
def health(request):
    return render(request,'health.html')

#terms & condition
def terms_conditions(request):
    return render(request,'terms_co.html')

@login_required
def myAccount(request):
    return render(request,'myaccount.html')
def documentation(request):
    apiname=request.GET.get('api','')
    if apiname:
        apiN=ApiDocumentation.objects.filter(short_name=apiname).first()
        if apiN:
            context={
                'api_name':apiN.api_name,
                'api_intro':apiN.api_intro,
                'endpoints':ApiEndpoints.objects.filter(api_name=apiN).all()
            }
            return render(request, 'apidocumentation.html', context=context)
        else:
            return redirect('browse')
    else:
        return redirect('browse')
