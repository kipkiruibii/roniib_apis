from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string
import requests
from django.http import JsonResponse
import traceback
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
import geocoder


def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code


def home(request):
    return render(request, 'index.html')


def pricing(request):
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": 'checkout@roniib.com',
        "custom": request.user.username,
        "a3": "29",
        "p3": 1,
        "t3": "M",
        "src": "1",
        "sra": "1",
        "no_note": "1",
        "item_name": "Developer Subscription",
        "notify_url": request.build_absolute_uri(reverse('paypal_notification')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
    }
    paypal_dict1 = {
        "cmd": "_xclick-subscriptions",
        "business": 'checkout@roniib.com',
        "custom": request.user.username,
        "a3": "69",
        "p3": 1,
        "t3": "M",
        "src": "1",
        "sra": "1",
        "no_note": "1",
        "item_name": "Enterprise Subscription",
        "notify_url": request.build_absolute_uri(reverse('paypal_notification')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
    }

    developer = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    enterprise = PayPalPaymentsForm(initial=paypal_dict1, button_type="subscribe")
    context = {"developer": developer,
               "enterprise": enterprise
               }
    return render(request, "pricing.html", context)


def move_page():
    pass


@csrf_exempt
def payment_successful(request):
    return render(request, "payment_successful.html")


@csrf_exempt
def payment_failed(request):
    return render(request, "payment_failed.html")


@csrf_exempt
def paypal_notification(request):
    if request.method == "POST":
        data = request.POST
        try:
            payment_status = data.get('payment_status', '')
            currency = data.get('mc_currency', '')
            amount = data.get('mc_gross', '')
            email = data.get('payer_email', '')
            transaction_id = data.get('txn_id', '')
            transaction_subject = data.get('transaction_subject', '')
            payment_date = data.get('payment_date', '')
            receiver_email = data.get('receiver_email', '')
            profile_id = data.get('subscr_id', '')
            userDetails = request.POST.get('custom', '')

            status = False
            subtype = 'Null'

            if payment_status == 'Completed':
                if userDetails:
                    user_paying = User.objects.filter(username=userDetails).first()
                    if user_paying:
                        if currency == 'USD':
                            if float(amount) >= 29:
                                status = True
                                subtype = 'Developer'
                                url = f'https://api.roniib.com/r-api-end/receiveSubscription/?username={user_paying.username}&subtype={subtype}'
                                requests.get(url)
                            elif float(amount) >= 69:
                                status = True
                                subtype = 'Enterprise'
                                url = f'https://api.roniib.com/r-api-end/receiveSubscription/?username={user_paying.username}&subtype={subtype}'
                                requests.get(url)
                            us = UserTransactions(
                                user=user_paying,
                                subscriber_id=profile_id,
                                receiver_email=receiver_email,
                                payment_date=payment_date,
                                transactionId=transaction_id,
                                subscription_type=subtype,
                                amount=amount,
                                is_successful=status
                            )
                            us.save()

                            subject = 'Successful subscription'
                            message = (
                                f'Hello {user_paying.username},\nYour subscription to Roniib API {subtype} plan was '
                                f'successful.\n'
                                f"Incase you need assistance or query don't hesitate to contact our support team."
                                f"Click here to get started https://www.roniib.com/myaccount ")
                            from_email = 'support@roniib.com'
                            recipient_list = [user_paying.email]
                            send_mail(subject, message, from_email, recipient_list)

        except:
            traceback.print_exc()

    return render(request, "index.html")


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
        # delete user tokens and other credentials from the api.roniib.com
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
            login(request, user)

            if not usr.is_verified:
                user_email = user.email
                context = {
                    'is_verified': False,
                    'email': user_email
                }
                return render(request, 'verificationpage.html', context=context)
            else:
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
                    usdet = UserDetails(
                        user=user
                    )
                    usdet.save()
                    sendVerMail(request, request.user.username, request.user.email)
                    if len(DayData.objects.filter(user=request.user)) < 30:
                        updateDayData(request.user)

                    if len(HourData.objects.filter(user=request.user)) < 24:
                        updateHourData(request.user)

                return redirect('verify')
            else:
                message = 'An account with this username/email already exists. Please try a different one'
                return render(request, 'register.html', context={'message': message})
        except:
            return render(request, 'register.html')

    return render(request, 'register.html')


def contact(request):
    context = {
        'mess': ''
    }
    if request.method == 'POST':
        is_member = False
        if request.user.is_authenticated:
            is_member = True
        email = request.POST['email']
        message = request.POST['message']

        un = CustomerQueries(
            email=email,
            is_member=is_member,
            message=message
        )
        un.save()
        context = {
            'mess': 'Successful! Your message has been sent'
        }

    return render(request, 'contact.html', context)


# terms & condition
def terms_conditions(request):
    return render(request, 'terms_co.html')


@csrf_exempt
def generateNewToken(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            url = f"https://api.roniib.com/r-api-end/generateNewToken/?username={request.user.username}"
            response = requests.get(url).json()
            token = response['token']
            ud = UserDetails.objects.filter(user=request.user).first()
            ud.api_key = token
            ud.date_created = datetime.now(timezone.utc)
            ud.save()
            datecreated = datetime.now(timezone.utc)
            dt = datecreated.strftime("%d/%m/%Y at %H:%M UTC")
            response_data = {
                'result': token,
                'datec': dt
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'result': 'Try again'})
    else:
        return JsonResponse({'result': 'Try again'})


def updateHourData(request):
    usr = request.user
    _time_ = datetime.now(timezone.utc)
    tms = []
    for i in range(24):
        tms.append(i)
    tms.reverse()
    for r_ in tms:
        _t_diff_ = _time_ - timedelta(hours=r_)
        for t in HourData.objects.filter(user=usr):
            if t.formatted_time.hour == _t_diff_.hour and t.formatted_time.month == _t_diff_.month and t.formatted_time.day == _t_diff_.day:
                continue
        else:
            hd = HourData(
                user=usr,
                count=0,
                formatted_time=_t_diff_,
                error_count=0

            )
            hd.save()
    user_h_data = HourData.objects.filter(user=usr)
    for t in user_h_data:
        tim = t.formatted_time
        _df = (_time_ - tim).total_seconds() / 3600
        if _df > 24:
            t.delete()


def updateDayData(request):
    usr = request.user
    _time_ = datetime.now(timezone.utc)
    tms = []
    for i in range(30):
        tms.append(i)
    tms.reverse()
    for r_ in tms:
        _t_diff_ = _time_ - timedelta(days=r_)
        for t in DayData.objects.filter(user=usr):
            if t.formatted_time.day == _t_diff_.day and t.formatted_time.month == _t_diff_.month:
                continue
        hd = DayData(
            user=usr,
            count=0,
            formatted_time=_t_diff_,
            error_count=0

        )
        hd.save()
    user_d_data = DayData.objects.filter(user=usr)
    for t in user_d_data:
        tim = t.formatted_time
        _df = (_time_ - tim).days
        if _df > 30:
            t.delete()


def getLast24hrs(offset, request):
    current_datetime = datetime.now()
    dte_list = [0 for i in range(24)]
    val_l = [0 for i in range(24)]

    if request.user.is_authenticated:
        dte_list = []
        val_l = []
        fd = HourData.objects.filter(user=request.user)
        if len(fd) < 24:
            updateHourData(request)

        for r in range(23):
            one_hour_ago = current_datetime - timedelta(hours=r)
            pres = False
            for r_i in HourData.objects.filter(user=request.user).order_by('-formatted_time'):
                if r_i.formatted_time.hour == one_hour_ago.hour and r_i.formatted_time.day == one_hour_ago.day and r_i.formatted_time.month == one_hour_ago.month:
                    val_l.append(r_i.count)
                    pres = True
                    break
            if not pres:
                val_l.append(0)
            frmt = int(one_hour_ago.strftime('%H'))
            frmt += offset
            val = f'{frmt}:00'
            if frmt < 10:
                val = f'0{frmt}:00'
            if frmt > 23:
                diff = frmt - 24
                val = f'0{0 + diff}:00'

            dte_list.append(val)
        val_l = val_l[::-1]
        dte_list = dte_list[::-1]
    return dte_list, val_l


def getLast7days(request):
    current_datetime = datetime.now()
    dte_list = ['0' for i in range(7)]
    val_l = [0 for i in range(7)]

    if request.user.is_authenticated:
        dte_list = []
        val_l = []
        fd = DayData.objects.filter(user=request.user)
        if len(fd) < 30:
            updateDayData(request)
        for r in range(29):
            if len(val_l) > 7:
                break
            days_ago = current_datetime - timedelta(days=r)
            pres = False
            for r_i in DayData.objects.filter(user=request.user).order_by('formatted_time'):
                if r_i.formatted_time.day == days_ago.day and r_i.formatted_time.month == days_ago.month:
                    val_l.append(r_i.count)
                    pres = True
                    break
            if not pres:
                val_l.append(0)

            frmt = days_ago.strftime('%a (%d)')
            dte_list.append(frmt)
        dte_list = dte_list[::-1]
        val_l = val_l[::-1]

    return dte_list, val_l


def getLast30Days(request):
    current_datetime = datetime.now()
    dte_list = ['0' for i in range(30)]
    val_l = [0 for i in range(30)]
    if request.user.is_authenticated:
        dte_list = []
        val_l = []
        fd = DayData.objects.filter(user=request.user)
        if len(fd) < 30:
            updateDayData(request)
        for r in range(29):
            days_ago = current_datetime - timedelta(days=r)
            pres = False
            for r_i in DayData.objects.filter(user=request.user).order_by('formatted_time'):
                if r_i.formatted_time.day == days_ago.day and r_i.formatted_time.month == days_ago.month:
                    val_l.append(r_i.count)
                    pres = True
                    break
            if not pres:
                val_l.append(0)

            frmt = days_ago.strftime('%d/%m')
            dte_list.append(frmt)
        dte_list = dte_list[::-1]
        val_l = val_l[::-1]
    return dte_list, val_l


@login_required
@csrf_exempt
def myAccount(request):
    lat = 0
    calls = 0
    err = 0
    error = CallErrors.objects.filter(user=request.user).first()
    c_s = DailyCounter.objects.filter(user=request.user).first()
    if c_s:
        calls = c_s.count
        if calls > 0:
            usr = UserTokens.objects.filter(user=request.user).first()
            if usr:
                sl = usr.subscription_level
                rt = usr.requests_count
                if sl == 'Basic':
                    i_c = 100
                    r_t = i_c - rt
                elif sl == 'Developer':
                    i_c = 300000
                    r_t = i_c - rt
                else:
                    i_c = 1000000
                    r_t = i_c - rt

                number = (r_t / i_c) * 100
                lat = "{:.1f}".format(number)
    if error:
        if calls > 0:
            er = error.count
            number = (er / calls) * 100
            err = "{:.2f}".format(number)

    client_ip = request.META.get('REMOTE_ADDR')
    location = geocoder.ip(client_ip)
    timezone_name = location.raw.get('timezone')
    try:
        client_timezone = pytz.timezone(timezone_name)
        offset = client_timezone.utcoffset(datetime.now())
        offset_hours, offset_minutes = divmod(offset.seconds // 60, 60)
    except pytz.UnknownTimeZoneError:
        offset_hours = 0

    graph_x_dat, graph_y_dat = getLast24hrs(offset_hours, request)
    if request.method == 'POST':
        type_e = request.POST.get('type')
        if type_e == 'seven':
            val = 0
            errs = 0
            for i in DayData.objects.filter(user=request.user).order_by('-formatted_time')[:7]:
                val += i.count
                errs += i.error_count
            calls = val
            number = (errs / calls) * 100
            err = "{:.2f}".format(number)

            graph_x_dat, graph_y_dat = getLast7days(request)
        elif type_e == 'thirty':
            val = 0
            errs = 0
            for i in DayData.objects.filter(user=request.user).order_by('-formatted_time')[:30]:
                val += i.count
                errs += i.error_count
            calls = val
            number = (errs / calls) * 100
            err = "{:.2f}".format(number)

            graph_x_dat, graph_y_dat = getLast30Days(request)
        else:
            graph_x_dat, graph_y_dat = getLast24hrs(offset_hours, request)
        return JsonResponse({'x_values': graph_x_dat,
                             'y_values': graph_y_dat,
                             'lat': f'{lat}%',
                             'err': f'{err}%',
                             'calls': f'{calls}',
                             })

    usr = UserDetails.objects.filter(user=request.user).first()
    currplan = 'Basic'
    if not usr.is_verified:
        user_email = request.user.email
        context = {
            'is_verified': False,
            'email': user_email
        }
        return render(request, 'verificationpage.html', context=context)

    if usr.api_key == 'to be stored later':
        apitoken = 'absent'
        dt = ''
        dtc = ''
    else:
        apitoken = usr.api_key
        datecreated = usr.date_created
        dt = datecreated.strftime("%d/%m/%Y at %H:%M UTC")
        lastt = UserTransactions.objects.filter(user=request.user).first()

        dtc = ''
        if lastt:
            lt = lastt.dateSub + relativedelta(months=1)
            dtc = lt.strftime("%d/%m/%Y")
            currplan = lastt.subscription_type

    context = {
        'apitoken': apitoken,
        'datecreated': dt,
        'transactions': UserTransactions.objects.filter(user=request.user),
        'last_transactions': dtc,
        'current_plan': currplan,
        'notifications': UserNotifications.objects.filter(user=request.user),
        'lat': lat,
        'err': err,
        'calls': calls,
        'graph_x_dat': graph_x_dat,
        'graph_y_dat': graph_y_dat,

    }
    return render(request, 'myaccount.html', context=context)


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

                url = f"https://api.roniib.com/r-api-end/generateToken/?username={request.user.username}"
                response = requests.get(url).json()
                token = response['token']
                ud = UserDetails.objects.filter(user=request.user).first()
                ud.api_key = token
                ud.save()

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
