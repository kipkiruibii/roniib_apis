from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User

from django.core.mail import send_mail
import mimetypes
import random
import string


def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code


# Create your views here.
def home(request):
    return render(request, 'index.html')


def pricing(request):
    return render(request, 'pricing.html')


def move_page():
    pass


def sendVerMail(request, username, email):
    try:
        rc = generate_random_code()
        usrr = UserDetails.objects.filter(user=request.user).first()
        if usrr:
            usrr.verf_code = rc
            usrr.save()

        message = (f"Hello {username},\nTo verify your email address and secure your account, please use the "
                   f"following 6-character\n \nverification code:{rc} \n\nSimply copy this code "
                   "and paste it on our website to complete the verification process.\n\nThank you for choosing "
                   "us.\n\nBest regards,\nRoniib Team")
        subject = 'Email Verification Code for Your Account'
        message = message
        from_email = 'support@roniib.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        return 'success'
    except Exception as e:
        return str(e)


def change_email(request):
    if request.user.is_authenticated:
        User.objects.filter(username=request.user.username).first().delete()
    return redirect('register')


def request_ver_link(request):
    if request.user.is_authenticated:
        usr = UserDetails.objects.filter(user=request.user).first()
        if not usr.is_verified:
            user_email = request.user.email

            val = sendVerMail(request, request.user.username, user_email)
            isMessPositive = True,
            disp_message = 'Verification link has been sent to your email. Check your inbox or spam box'
            if val != 'success':
                isMessPositive = False
                disp_message = f'Failed {val}'

            context = {
                'is_verified': False,
                'email': user_email,
                'isMessPositive': isMessPositive,
                'disp_message': disp_message
            }
            return render(request, 'verificationpage.html', context=context)
    else:
        return redirect('apicategories')


def log_in(request):
    if request.user.is_authenticated:
        return redirect('apicategories')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            usr = UserDetails.objects.filter(user=user).first()
            if not usr.is_verified:
                user_email = request.user.email
                context = {
                    'is_verified': False,
                    'email': user_email
                }
                return render(request, 'verificationpage.html', context=context)
            else:
                login(request, user)
                return redirect('apicategories')
        else:
            message = 'Invalid credentials. Try again'
            return render(request, 'login.html', context={'message': message})

    else:
        return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('apicategories')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.filter(username=username)
            if not user:
                User.objects.create_user(username=username, email=email, password=password)

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    sendVerMail(request, request.user.username, request.user.email)
                    usdet = UserDetails(
                        user=user,
                        api_key='to be stored later'
                    )
                    usdet.save()

                return redirect('verify')
            else:
                message = 'An account with this username/email already exists. Please try a different one'
                return render(request, 'register.html', context={'message': message})
        except:
            return render(request, 'register.html')

    return render(request, 'register.html')


def contact(request):
    return render(request, 'contact.html')


# terms & condition
def terms_conditions(request):
    return render(request, 'terms_co.html')


@login_required
def myAccount(request):
    usr = UserDetails.objects.filter(user=request.user).first()
    if not usr.is_verified:
        user_email = request.user.email
        context = {
            'is_verified': False,
            'email': user_email
        }
        return render(request, 'verificationpage.html', context=context)

    return render(request, 'myaccount.html')


def documentation(request):
    apiname = request.GET.get('api', '')
    if apiname:
        apiN = ApiDocumentation.objects.filter(short_name=apiname).first()
        if apiN:
            context = {
                'api_name': apiN.api_name,
                'api_intro': apiN.api_intro,
                'endpoints': ApiEndpoints.objects.filter(api_name=apiN).all()
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
        subgroup = items[i:i + subgroup_size]
        subgroups.append(subgroup)

    return subgroups


def apicategories(request):
    category = request.GET.get('category', '')
    recommended = []
    popular = ApiDocumentation.objects.all().order_by('-api_subscribers')[:3]
    rc = ApiDocumentation.objects.all().order_by('-api_total_requests')

    count = 0
    for r in rc:
        if count >= 3:
            break
        if r not in popular:
            recommended.append(r)
            count += 1
    context = {
        'categories': APICategories.objects.all(),
        'popular': popular,
        'recommended': recommended,
    }
    if category:
        cat = APICategories.objects.filter(category_short=category).first()
        if cat:
            context = {
                'categories': APICategories.objects.all(),
                'selected_category': group_into_subgroups(ApiDocumentation.objects.filter(api_category=cat)),
                'selected_category_mob': ApiDocumentation.objects.filter(api_category=cat),
                'selected_category_name': cat.category,
            }
    return render(request, 'apicategories.html', context=context)


def verificationPage(request):
    if request.method == 'POST':
        verfcode = request.POST['verfcode']

        saved_ver = UserDetails.objects.filter(user=request.user).first()
        if saved_ver:
            verifyc = saved_ver.verf_code
            if verifyc == verfcode:
                saved_ver.is_verified = True
                saved_ver.save()
                return redirect('apicategories')
            else:
                context = {
                    'is_verified': False,
                    'email': request.user.email,
                    'isMessPositive': False,
                    'disp_message': 'Failed: Try again'
                }

            return render(request, 'verificationpage.html', context=context)
        else:
            context = {
                'is_verified': False,
                'email': request.user.email,
            }
        return render(request, 'verificationpage.html', context=context)
    if request.user.is_authenticated:
        usr = UserDetails.objects.filter(user=request.user).first()
        if not usr.is_verified:
            user_email = request.user.email
            context = {
                'is_verified': False,
                'email': user_email
            }
        else:
            context = {
                'is_verified': True,
            }
        return render(request, 'verificationpage.html', context=context)
    else:
        return redirect('register')

