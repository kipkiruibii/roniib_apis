from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'index.html')
def pricing(request):
    return render(request,'pricing.html')

def move_page():
    pass

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('apicategories')
        else:
            message='Invalid credentials. Try again'
            return render(request, 'login.html',context={'message':message})

    else:
        return render(request,'login.html')

def log_out(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request,'register.html')
def contact(request):
    return render(request,'contact.html')
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
def group_into_subgroups(items):
    subgroups = []
    subgroup_size = 3

    for i in range(0, len(items), subgroup_size):
        subgroup = items[i:i+subgroup_size]
        subgroups.append(subgroup)

    return subgroups


def apicategories(request):
    category=request.GET.get('category','')
    recommended=[]
    popular=ApiDocumentation.objects.all().order_by('-api_subscribers')[:3]
    rc=ApiDocumentation.objects.all().order_by('-api_total_requests')

    count=0
    for r in rc:
        if count>=3:
            break
        if r not in popular:
            recommended.append(r)
            count+=1
    context={
        'categories': APICategories.objects.all(),
        'popular':popular,
        'recommended':recommended,
    }
    if category:
        cat=APICategories.objects.filter(category_short=category).first()
        if cat:
            context={
                'categories':APICategories.objects.all(),
                'selected_category':group_into_subgroups(ApiDocumentation.objects.filter(api_category=cat)),
                'selected_category_mob':ApiDocumentation.objects.filter(api_category=cat),
                'selected_category_name':cat.category,
            }
    return render(request,'apicategories.html',context=context)
