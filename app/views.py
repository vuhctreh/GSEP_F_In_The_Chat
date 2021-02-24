from __future__ import unicode_literals
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, createTaskForm
from django.contrib.auth.decorators import login_required
from .models import CoffeeUser, CafeTable, Message, Task
from operator import attrgetter


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


@login_required(login_url="/")
def set_tasks(request):
    user = request.user
    form = createTaskForm()

    if not user.is_staff:
        return redirect("home")

    context = {'form': form}
    if request.method == 'POST':
        form = createTaskForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context["createTaskForm"] = form
    return render(request, 'set_tasks.html', context)


@login_required(login_url="/")
def view_tasks(request):
    current_user = request.user
    tables = CafeTable.objects.filter(
        university=current_user.university,
        table_id__in=current_user.cafe_table_ids.values_list('table_id', flat=True)
    )
    tasks = Task.objects.filter(table_id__in=tables)
    context = {
        'tasks': tasks
    }
    if request.method == 'POST':
        return redirect("viewtasks")
    return render(request, 'view_tasks.html', context)


@login_required(login_url='/')
def dashboard(request):
    user = CoffeeUser.objects.get(id=request.user.id)
    context = {
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'university': user.get_university_display(),
        'dateJoined': user.date_joined,
        'points': user.points,
    }
    return render(request, "dashboard.html", context)


@login_required(login_url='/')
def leaderboard(request):
    users = CoffeeUser.objects.all()
    if len(users) > 10:
        users = users[:9]
    sorted_users = sorted(users, key=attrgetter("points"), reverse=True)
    context = {
        'users': sorted_users,
    }
    return render(request, "leaderboard.html", context)


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
