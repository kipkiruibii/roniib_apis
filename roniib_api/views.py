from email.mime.image import MIMEImage

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
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
from django.core.mail import EmailMultiAlternatives


def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code


def home(request):
    return render(request, 'index.html')


def resendResetCode(request):
    if request.method == "POST":
        pass

    pass


def reset_password_code(request):
    email = ''
    messg = ''
    val = request.GET.get('email_addr', None)
    if val:
        user = User.objects.filter(email__exact=val).first()
        if user:
            email = EmailMultiAlternatives(
                subject='Password Reset Verification Code',
                body='Plain text version of the email (optional)',
                from_email='support@roniib.com',
                to=[val],
            )
            rc = generate_random_code()

            PasswordReset.objects.filter(user=user).delete()
            m = PasswordReset(
                user=user,
                reset_code=rc
            )
            m.save()

            context = {
                'user': user.username,
                'verf_code': rc,
            }

            html_content = render_to_string('password_reset_email.html', context=context)
            email.attach_alternative(html_content, 'text/html')

            image_path = '/home/roninkhl/mainapplication/roniib_api/static/images/roniib_logo.png'
            email.mixed_subtype = 'related'
            image_file = open(image_path, 'rb')
            email_image = MIMEImage(image_file.read())
            email_image.add_header('Content-ID', '<custom_image>')
            email.attach(email_image)
            email.send()
            context = {
                'failed': False,
                'message': 'Sent',
                'isVerf': True,
                'email_ad': val,
                'stage_2': True
            }
        else:
            context = {
                'failed': True,
                'message': 'Failed to send',
                'stage_2': True

            }
        return render(request, 'reset_password_code.html', context)

    if request.method == "POST":
        emaily = request.POST.get('email', None)
        if emaily:
            try:
                user = User.objects.filter(email__exact=emaily).first()
                if user:

                    email = EmailMultiAlternatives(
                        subject='Password Reset Verification Code',
                        body='Plain text version of the email (optional)',
                        from_email='support@roniib.com',
                        to=[emaily],
                    )
                    rc = generate_random_code()

                    PasswordReset.objects.filter(user=user).delete()
                    m = PasswordReset(
                        user=user,
                        reset_code=rc
                    )
                    m.save()

                    context = {
                        'user': user.username,
                        'verf_code': rc,
                    }

                    html_content = render_to_string('password_reset_email.html', context=context)
                    email.attach_alternative(html_content, 'text/html')

                    image_path = '/home/roninkhl/mainapplication/roniib_api/static/images/roniib_logo.png'
                    email.mixed_subtype = 'related'
                    image_file = open(image_path, 'rb')
                    email_image = MIMEImage(image_file.read())
                    email_image.add_header('Content-ID', '<custom_image>')
                    email.attach(email_image)
                    email.send()
                    context = {
                        'failed': False,
                        'message': 'Enter the verification code sent to your email below',
                        'isVerf': True,
                        'email_ad': emaily,
                        'stage_2': True
                    }
                else:
                    context = {
                        'failed': True,
                        'message': 'No account associated with the email address provided',

                    }
                return render(request, 'reset_password_code.html', context)

            except:
                traceback.print_exc()
        verfc = request.POST.get('verifycd', None)
        if verfc:
            eml = request.POST.get('eml', None)
            user = User.objects.filter(email__exact=eml).first()

            m = PasswordReset.objects.filter(user=user, reset_code=verfc).first()
            if m:
                context = {
                    'failed': False,
                    'message': "Let's set up a new password",
                    'isVerf': True,
                    'email_ad': eml,
                    'stage_3': True
                }

                return render(request, 'reset_password_code.html', context=context)
            else:
                context = {
                    'failed': True,
                    'message': 'Invalid code',
                    'stage_2': True
                }
                return render(request, 'reset_password_code.html', context)

        passw1 = request.POST.get('pass1', None)
        passw2 = request.POST.get('pass2', None)
        eml = request.POST.get('eml', None)
        if passw1 and passw1:
            if passw1 == passw2:
                user = User.objects.filter(email__exact=eml).first()
                if user:
                    user.set_password(passw1)
                    user.save()
                    PasswordReset.objects.filter(user=user).delete()
                    context = {
                        'stage_4': True
                    }
                else:
                    context = {
                        'failed': True,
                        'message': 'Please check your passwords and try again',
                        'stage_3': True
                    }
                return render(request, 'reset_password_code.html', context)
            else:
                context = {
                    'failed': True,
                    'message': 'Please check your passwords and try again',
                    'stage_3': True
                }
                return render(request, 'reset_password_code.html', context)

    context = {
        'user': '',
        'message': messg
    }

    return render(request, 'reset_password_code.html', context=context)


def reset_password(request):
    return render(request, 'reset_password.html')


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
            val = email

            email = EmailMultiAlternatives(
                subject='Account Verification',
                body='Plain text version of the email (optional)',
                from_email='support@roniib.com',
                to=[val],
            )

            context = {
                'user': usrr.user.username,
                'verf_code': rc,
            }

            html_content = render_to_string('welcome_email.html', context=context)
            email.attach_alternative(html_content, 'text/html')

            image_path = '/home/roninkhl/mainapplication/roniib_api/static/images/roniib_logo.png'
            email.mixed_subtype = 'related'
            image_file = open(image_path, 'rb')
            email_image = MIMEImage(image_file.read())
            email_image.add_header('Content-ID', '<custom_image>')
            email.attach(email_image)
            email.send()
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
            isMessPositive = True
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
                    val = sendVerMail(request, request.user.username, request.user.email)
                    isMessPositive = True
                    disp_message = 'Verification link has been sent to your email. Check your inbox or spam box'
                    if val != 'success':
                        isMessPositive = False
                        disp_message = f'Failed {val}'

                    context = {
                        'is_verified': False,
                        'email': email,
                        'isMessPositive': isMessPositive,
                        'disp_message': disp_message
                    }
                    return render(request, 'verificationpage.html', context=context)
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
            if t.formatted_time.hour == _t_diff_.hour:
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
    errors = 0
    calls = 0

    if request.user.is_authenticated:
        dte_list = []
        val_l = []
        fd = HourData.objects.filter(user=request.user)
        if len(fd) < 24:
            updateHourData(request)

        for r in range(24):
            one_hour_ago = current_datetime - timedelta(hours=r)
            pres = False
            for r_i in HourData.objects.filter(user=request.user).order_by('-formatted_time'):
                if r_i.formatted_time.hour == one_hour_ago.hour and r_i.formatted_time.day == one_hour_ago.day and r_i.formatted_time.month == one_hour_ago.month:
                    val_l.append(r_i.count)
                    calls += r_i.count
                    errors += r_i.error_count
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
    return dte_list, val_l, errors, calls


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
        for r in range(7):
            # if len(val_l) > 7:
            #     break
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
        for r in range(30):
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
    i_c = 1
    usr = UserTokens.objects.filter(user=request.user).first()
    if usr:
        sl = usr.subscription_level
        if sl == 'Enterprise':
            i_c = 1000000
        elif sl == 'Developer':
            i_c = 300000
        else:
            i_c = 100
    client_ip = request.META.get('REMOTE_ADDR')
    location = geocoder.ip(client_ip)
    timezone_name = location.raw.get('timezone')
    try:
        client_timezone = pytz.timezone(timezone_name)
        offset = client_timezone.utcoffset(datetime.now())
        offset_hours, offset_minutes = divmod(offset.seconds // 60, 60)
    except pytz.UnknownTimeZoneError:
        offset_hours = 0

    graph_x_dat, graph_y_dat, errors, calls = getLast24hrs(offset_hours, request)
    err = 0
    number = (calls / i_c) * 100
    lat = "{:.2f}".format(number)
    if calls > 0:
        number = (errors / calls) * 100
        err = "{:.2f}".format(number)
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
            graph_x_dat, graph_y_dat, errors, calls = getLast24hrs(offset_hours, request)
        return JsonResponse({'x_values': graph_x_dat,
                             'y_values': graph_y_dat,
                             'lat': f'{lat}%',
                             'err': f'{err}%',
                             'calls': f'{calls}',
                             })

    usr = UserDetails.objects.filter(user=request.user).first()
    isLate = False

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
        lastt = UserTransactions.objects.filter(user=request.user, is_successful=True).last()

        dtc = ''
        if lastt:
            lt = lastt.dateSub + relativedelta(months=1)
            dtc = lt.strftime("%d/%m/%Y")
            currplan = lastt.subscription_type

            tn = datetime.now(timezone.utc) - lt
            if tn.total_seconds() > 0:
                isLate = True

    context = {
        'apitoken': apitoken,
        'datecreated': dt,
        'transactions': UserTransactions.objects.filter(user=request.user).order_by('-pk'),
        'last_transactions': dtc,
        'current_plan': currplan,
        'notifications': UserNotifications.objects.filter(user=request.user),
        'lat': lat,
        'err': err,
        'calls': calls,
        'isLate': isLate,
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
