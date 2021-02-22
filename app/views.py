from __future__ import unicode_literals
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostMessageForm
from django.contrib.auth.decorators import login_required
from .models import CoffeeUser, CafeTable, Message, Task


# Victoria: 18/2/21
def index(request):
    context = {}

    # if user is already authenticated they will be redirected to home
    # whenever they try to access /login until they logout
    user = request.user
    if user.is_authenticated:
        return redirect('table_view')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('table_view')

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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('table_view')
        else:
            context['form'] = form
    else:  # get request
        form = SignUpForm()
        context['form'] = form
    return render(request, 'sign_up.html', context)


# Isabel: 18/2/21
@login_required(login_url='/')
def table_view(request):
    current_user = request.user
    # tables with correct interests and university for user
    tables = CafeTable.objects.filter(
        university=current_user.university,
        table_id__in=current_user.cafe_table_ids.values_list('table_id',
                                                             flat=True)
    )
    context = {
        'tables': tables
    }
    return render(request, "table_view.html", context)


# Isabel: 18/2/21
@login_required(login_url='/')
def table_chat(request, pk):
    try:
        table = CafeTable.objects.get(pk=pk)
    except CafeTable.DoesNotExist:
        return render(request, 'denied.html')
    # make sure user can only access their tables
    current_user = request.user
    if ((current_user.university != table.university) or
       (table.table_id not in
       current_user.cafe_table_ids.values_list('table_id', flat=True))):
        return render(request, 'denied.html')
    # if post req, use the form to add the msg
    if request.method == 'POST':
        form = PostMessageForm(request.POST)
        if form.is_valid():
            message_content = form.cleaned_data.get('message_content')
            msg = Message.objects.create(
                table_id=table,
                created_by=current_user,
                message_content=message_content,
            )
    else:
        form = PostMessageForm()
    # show the existing messages by querying db
    messages = Message.objects.filter(table_id=table).order_by('message_date')[:100]
    #IMPORTANT: we probs should not be loading every msg ever, later we should
    # add a feature to load more when required
    # get the tasks for the table
    tasks = Task.objects.filter(table_id=table).order_by('task_date')
    # get all the users in the table
    users = table.coffeeuser_set.all()
    # final
    context = {
        "table": table,
        "form": form,
        "messages": messages,
        "users": users,
        "tasks": tasks
    }
    return render(request, "table_chat.html", context)


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
