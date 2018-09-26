from django.shortcuts import render, redirect


def index(request):
    return render(request, 'login/index.html')


def login(request):
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')


def logout(request):
    return redirect('/index/')
