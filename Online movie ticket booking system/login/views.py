from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from home.models import UserInfo
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import *


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/login/loggedin/')
    else:
        c = {}
        c.update(csrf(request))
        c.update({"error": True})
        return render_to_response('login.html', c)


def adduser(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("signup.html", c)


def signup(request):
    unm = request.POST.get('username', '')
    pas = request.POST.get('password', '')
    dob = request.POST.get('dob', '')
    mob = request.POST.get('mob', '')
    fullname = request.POST.get('fullname', '')
    repas = request.POST.get('rpassword', '')
    email = request.POST.get('email', '')
    if repas == pas:
        s = User.objects.create_user(username=unm, password=pas, email=email)
        p = UserInfo(userid=s, fullname=fullname, dob=dob, mob=mob)
        s.save()
        p.save()
        return HttpResponseRedirect('/login/login/')
    else:
        messages.warning(request, 'Password fileds does not match')
        return HttpResponseRedirect('/login/adduser/')


def signedup(request):
    return render_to_response('login.html', {"full_name": request.user.username, 'signup': True})


def loggedin(request):
    return render_to_response('home.html', {"full_name": request.user.username})


def invalidlogin(request):
    return render_to_response('invalidlogin.html')


def logout(request):
    c = {}
    c.update(csrf(request))
    auth.logout(request)
    return render_to_response('login.html', c)


def profile(request):
    s = UserInfo.objects.get(userid=request.user)
    return render_to_response('profile.html', {"uname": request.user.username, "fullname": s.fullname, "dob": s.dob,
                                               "email": request.user.email, "mob": s.mob})


def profileupdate(request):
    c = {}
    c.update(csrf(request))
    s = UserInfo.objects.get(userid=request.user)
    c.update({"uname": request.user.username, "email": request.user.email, "mob": s.mob})
    return render_to_response('profileupdate.html', c)


def update(request):
    user = request.user
    s = UserInfo.objects.get(userid=request.user)
    #unm = request.POST.get('name', '')
    email = request.POST.get('email', '')
    mob = request.POST.get('mob', '')
    #user.username = unm
    user.email = email
    user.save()
    s.mob = mob
    s.save()
    return HttpResponseRedirect('/login/login')


def tickets(request):
    c = {}
    c.update(csrf(request))
    t = Tickets.objects.filter(username=request.user.username)
    c.update({"t": t})
    return render_to_response('tickets_show.html', c)
