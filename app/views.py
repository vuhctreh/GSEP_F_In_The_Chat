from __future__ import unicode_literals
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required


# Victoria: 18/2/21
def index(request):
    context = {}

    # if user is already authenticated they will be redirected to home
    # whenever they try to access /login until they logout
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')

        else:
            context['login_form'] = form

    else:
        form = LoginForm()
        context['login_form'] = form
    return render(request, 'login.html', context)


def log_out(request):
    logout(request)
    return redirect('/')


# Isabel: 18/2/21
def signup(request):
    context = {}
    if request.method == 'POST':  # change to if request.POST    ??
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context['form'] = form
    else:  # get request
        form = SignUpForm()
        context['form'] = form
    return render(request, 'sign_up.html', context)


@login_required(login_url='/')
def cafe_home(request):
    return render(request, 'cafe_home.html')

def tasks(request):
    return render(request, 'tasks.html')

def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')
