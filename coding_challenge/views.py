import secrets
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from apps.profil.backends import EmailAuthBackend
from apps.profil.models import CustomUser


def authentification(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "login.html", {})
        elif request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = EmailAuthBackend().authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop/index')
            elif user is None:
                return render(request, "login.html", {'fail': True})
    else:
        return redirect('shop/index')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "register.html", )
        elif request.method == 'POST':
            if request.POST.get('password') == request.POST.get('password_confirm'):
                username = secrets.token_hex(5)
                password = make_password(request.POST.get('password'))
                c = CustomUser(email=request.POST.get('email'), password=password, username=username)
                c.save()
                login(request, c)
                return redirect('../shop/index')
    else:
        return redirect('shop/index')


def deconnexion(request):
    logout(request)
    return redirect('authentification')
