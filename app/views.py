from __future__ import unicode_literals
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostMessageForm, CUserEditForm
from django.contrib.auth.decorators import login_required
from .models import CoffeeUser, CafeTable, Message, Task
import datetime
from operator import attrgetter


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
        if form.is_valid() and form.cleaned_data.get('accept_terms'):
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
            task_name = form.cleaned_data.get('task_name')
            table_id = form.cleaned_data.get('table_id')
            task_content = form.cleaned_data.get('task_content')
            points = form.cleaned_data.get('points')
            task = Task.objects.create(
                task_name=task_name,
                created_by=user,
                table_id=table_id,
                task_content=task_content,
                points=points,
            )
        else:
            context["createTaskForm"] = form
    else:
        context["createTaskForm"] = form
    return render(request, 'set_tasks.html', context)


@login_required(login_url="/")
def view_tasks(request):
    current_user = request.user
    # get the tables the current user is part of
    tables = CafeTable.objects.filter(
        university=current_user.university,
        table_id__in=current_user.cafe_table_ids.values_list('table_id',
                                                             flat=True)
    )
    # get the tasks corresponding to these tables that the user hasn't done
    tasks = Task.objects.filter(table_id__in=tables).exclude(completed_by=current_user)
    context = {
        'tasks': tasks
    }
    return render(request, 'view_tasks.html', context)


@login_required(login_url='/')
def completeTask(request, pk):
    # Get the current user logged in
    current_user = request.user
    # Get the task for which the button is pressed
    completedTask = Task.objects.get(pk=pk)
    # Add user to completed by field in database
    completedTask.completed_by.add(current_user)
    # Increment points field by respective amount
    current_user.points += completedTask.points
    current_user.save()
    print("SUCCESS!")
    return redirect('/view_tasks')
    # return render(request, 'view_tasks.html')


@login_required(login_url='/')
def dashboard(request):
    user = CoffeeUser.objects.get(id=request.user.id)
    users = CoffeeUser.objects.all()
    if len(users) > 10:
        users = users[:9]
    sorted_users = sorted(users, key=attrgetter("points"), reverse=True)
    context = {
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'university': user.get_university_display(),
        'dateJoined': user.date_joined,
        'points': user.points,
        'users': sorted_users,
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
            task_name = form.cleaned_data.get('task_name')
            table_id = form.cleaned_data.get('table_id')
            task_content = form.cleaned_data.get('task_content')
            points = form.cleaned_data.get('points')
            task = Task.objects.create(
                task_name=task_name,
                created_by=user,
                table_id=table_id,
                task_content=task_content,
                points=points,
            )
        else:
            context["createTaskForm"] = form
    else:
        context["createTaskForm"] = form
    return render(request, 'set_tasks.html', context)


@login_required(login_url="/")
def view_tasks(request):
    current_user = request.user
    # get the tables the current user is part of
    tables = CafeTable.objects.filter(
        university=current_user.university,
        table_id__in=current_user.cafe_table_ids.values_list('table_id',
                                                             flat=True)
    )
    # get the tasks corresponding to these tables that the user hasn't done
    tasks = Task.objects.filter(table_id__in=tables).exclude(completed_by=current_user)
    context = {
        'tasks': tasks
    }
    return render(request, 'view_tasks.html', context)


@login_required(login_url='/')
def completeTask(request, pk):
    # Get the current user logged in
    current_user = request.user
    # Get the task for which the button is pressed
    completedTask = Task.objects.get(pk=pk)
    # Add user to completed by field in database
    completedTask.completed_by.add(current_user)
    # Increment points field by respective amount
    current_user.points += completedTask.points
    current_user.save()
    print("SUCCESS!")
    return redirect('/view_tasks')
    # return render(request, 'view_tasks.html')


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
            form = PostMessageForm()
    else:
        form = PostMessageForm()
    # show the existing messages by querying db
    messages = Message.objects.filter(table_id=table).order_by('message_date')[:100]
    #IMPORTANT: we probs should not be loading every msg ever, later we should
    # add a feature to load more when required
    # get the tasks for the table - new: only notified of tasks set in last 24h
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    tasks = Task.objects.filter(table_id=table,
                                task_date__gte=date_from).order_by('task_date')
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


# will and izzy
@login_required(login_url='/')
def edit_info(request):
    user = request.user
    if request.method == 'POST':
        form = CUserEditForm(request.POST)
        if form.is_valid():
            # save what is entered and validate
            if form.cleaned_data['first_name']:
                user.first_name = form.cleaned_data['first_name']

            if form.cleaned_data['last_name']:
                user.last_name = form.cleaned_data['last_name']

            if form.cleaned_data['year']:
                if form.cleaned_data['year'] >= 1:
                    user.year = form.cleaned_data['year']

            if form.cleaned_data['course']:
                if user.course:
                    old_course = user.course
                    # if already on a course, remove from old course table
                    old_table_name = "COURSE: " + old_course
                    table = user.cafe_table_ids.get(table_id=old_table_name)
                    user.cafe_table_ids.remove(table)

                new_course = form.cleaned_data['course'].lower()
                user.course = new_course
                # upper case throughout so not duplicates with different casing
                new_course_table_name = "COURSE: " + new_course
                # see if a table for this course exists
                try:
                    table = CafeTable.objects.get(
                        university=user.university,
                        table_id=new_course_table_name
                    )
                except CafeTable.DoesNotExist:
                    # if that table does not exist, create it
                    table = CafeTable.objects.create(
                        table_id=new_course_table_name,
                        university=user.university
                    )
                # add the user to the table
                user.cafe_table_ids.add(table)

            if form.cleaned_data['add_table_id']:
                add_table_id = form.cleaned_data['add_table_id'].lower()
                if not add_table_id.startswith("course:"):
                    # can't be sneaky and add urself to a course this way
                    # see if table already exists
                    try:
                        table = CafeTable.objects.get(
                            university=user.university,
                            table_id=add_table_id
                        )
                    except CafeTable.DoesNotExist:
                        # if that table does not exist, create it
                        table = CafeTable.objects.create(
                            table_id=add_table_id,
                            university=user.university
                        )
                    # add the user to the table
                    user.cafe_table_ids.add(table)

            if form.cleaned_data['remove_table_id']:
                # if it is actually in their list of tables, remove
                table_name_to_rm = form.cleaned_data['remove_table_id']
                #make lower again
                try:
                    table = user.cafe_table_ids.get(table_id=table_name_to_rm)
                    user.cafe_table_ids.remove(table)
                except CafeTable.DoesNotExist:
                    pass
            # end
            user.save()
            form = CUserEditForm()
    else:
        form = CUserEditForm()
    tables = user.cafe_table_ids.values_list('table_id', flat=True)
    context = {
        'user': user,
        'form': form,
        'tables': tables
    }
    return render(request, "edit_info.html", context)


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
