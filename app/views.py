from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostMessageForm, CUserEditForm, \
                   createTaskForm, StudyBreaksForm, CUserEditFormStaff, \
                   ReportForm
from django.contrib.auth.decorators import login_required
from .models import CoffeeUser, CafeTable, Message, Task, Report
import datetime
from operator import attrgetter
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from .small_scripts_def import check_points_treshold, how_much_to_go
import pytz

list_coffee_link = ["images/espresso.PNG", "images/americano.PNG", "images/cappuccino.PNG", "images/hot_chocolate.PNG", "images/latte.PNG", "images/mocha.PNG", "images/matcha.PNG", "images/frappuccino.PNG", "images/ice_tea.PNG", "images/bubble_tea.PNG"]
list_coffee_name = ["espresso", "americano", "cappuccino", "hot chocolate", "latte", "mocha", "matcha", "frappuccino", "ice tea", "bubble tea"]

# Isabel 3/3/21
def get_number_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    active = 0
    for session in active_sessions:
        data = session.get_decoded()
        if data != {}:
            active += 1
    return active


# Isabel 3/3/21
@login_required(login_url='/')
def get_msgs(request, table):
    # deal with if the requested table doesn't exist
    try:
        table = CafeTable.objects.get(pk=table)
    except CafeTable.DoesNotExist:
        return render(request, 'denied.html')
    # make sure user can only access their tables
    current_user = request.user
    if ((current_user.university != table.university) or
       (table.table_id not in
       current_user.cafe_table_ids.values_list('table_id', flat=True))):
        return render(request, 'denied.html')

    messages = Message.objects.filter(table_id=table).order_by('message_date')[:100]

    for msg in messages:
        msg.message_date = pytz.utc.localize(msg.message_date).isoformat()
    return render(request, 'messages.html', {'messages': messages})


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
        'tables': tables,
        'num_users': get_number_current_users()
    }
    return render(request, "table_view.html", context)


@login_required(login_url='/')
def dashboard(request):
    user = request.user

    users = CoffeeUser.objects.filter(is_staff=False)
    sorted_users = sorted(users, key=attrgetter("points"), reverse=True)
    if len(sorted_users) > 10:
        sorted_users = sorted_users[:9]

    if user.is_staff is False:
        # setting study breaks feature
        if request.method == 'POST':
            form = StudyBreaksForm(request.POST)
            if form.is_valid():
                mins = form.cleaned_data.get('minutes_studying_for')
                break_time = datetime.datetime.now() + \
                    datetime.timedelta(minutes=mins)
                user.studying_until = break_time
                user.save()

        # this derives an int from the points earned by the user,
        # the int corresponds to the name of the collectable's picture in the
        # files it then concatenates together: the int returned and the link to
        # the image which in the end gives a link to the collectable's image
        # corresponding to the number of points
        current_user_points = user.points
        pointsLevel = check_points_treshold(current_user_points)
        # getting the name from the list_coffee with the index for the current
        # max collectable
        link_img = list_coffee_link[int(pointsLevel)]
        name_coffee = list_coffee_name[int(pointsLevel)]

        # creating the list for the previous collectables
        previous_collectables = []
        index_list = 0
        while (index_list < int(pointsLevel)):
            previous_collectables.append(list_coffee_link[index_list])
            index_list += 1

        # calculating how many points to reach next collectable
        points_to_go_next_collectable = int(how_much_to_go(pointsLevel))

        # see if the user is currently studying
        if user.studying_until:
            if user.studying_until <= datetime.datetime.now():
                # they are not studying anymore
                user.studying_until = None
                user.save()
                studying = False
            else:
                studying = True
        else:
            studying = False

    else:  # staff user - don't waste computation on irrelevant stuff
        link_img = ''
        points_to_go_next_collectable = 0
        name_coffee = ''
        previous_collectables = []
        studying = False

    tz_date = pytz.utc.localize(user.date_joined).isoformat()

    context = {
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'university': user.get_university_display(),
        'dateJoined': tz_date,
        'points': user.points,
        'users': sorted_users,
        'collectable': link_img,
        'pointsToGo': points_to_go_next_collectable,
        'nameCollectable': name_coffee,
        'previousCollectables': previous_collectables,
        'listOfCoffeeLink': list_coffee_link,
        'num_users': get_number_current_users(),
        'break_form': StudyBreaksForm(),
        'studying': studying,
        'pk': user.pk,
        'staff': user.is_staff,
    }
    return render(request, "dashboard.html", context)


# Victoria 04 & 05/03/21
@login_required(login_url="/")
def set_tasks(request):
    user = request.user
    form = createTaskForm(user=request.user)

    tables = CafeTable.objects.filter(
        university=user.university,
        table_id__in=user.cafe_table_ids.values_list('table_id', flat=True))
    form.fields['table_id'].queryset = tables

    if user.tasks_set_today >= 2 and user.next_possible_set == datetime.date.today():
        user.tasks_set_today = 0
        user.save()

    if user.tasks_set_today >= 2 and not user.is_staff:
        return redirect("dashboard")

    context = {'form': form, 'num_users': get_number_current_users()}
    if request.method == 'POST':
        form = createTaskForm(request.POST, user=request.user)
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
                points=points
            )
            user.tasks_set_today += 1
            user.save()

            if user.tasks_set_today >= 2 and not user.is_staff:
                user.next_possible_set = datetime.date.today() + datetime.timedelta(days=1)
                user.save()
                return redirect("dashboard")

        else:
            context["createTaskForm"] = form
    else:
        context["createTaskForm"] = form
    return render(request, 'set_tasks.html', context)


@login_required(login_url="/")
def view_tasks(request):
    current_user = request.user
    if current_user.is_staff:
        return redirect("dashboard")
    # get the tables the current user is part of
    tables = CafeTable.objects.filter(
        university=current_user.university,
        table_id__in=current_user.cafe_table_ids.values_list('table_id',
                                                             flat=True)
    )
    # get the tasks corresponding to these tables that the user hasn't done
    tasks = Task.objects.filter(table_id__in=tables).exclude(completed_by=current_user).exclude(created_by=current_user)

    complete_current = []
    complete_total = []
    for task in tasks:
        current, total = task.get_number_completed_task()
        complete_current.append(current)
        complete_total.append(total)

    context = {
        'tasks': zip(tasks, complete_current, complete_total),
        'users': CoffeeUser.objects.all(),
        'num_users': get_number_current_users()
    }
    return render(request, 'view_tasks.html', context)


# Victoria 05/03/21
@login_required(login_url='/')
def completeTask(request, pk):
    # Get the current user logged in
    current_user = request.user
    # Get the task for which the button is pressed
    completedTask = Task.objects.get(pk=pk)

    if current_user.student_tasks_completed >= 2 and current_user.next_possible_complete == datetime.date.today():
        current_user.student_tasks_completed = 0
        current_user.save()

    if completedTask.created_by.is_staff:
        # Add user to completed by field in database
        completedTask.completed_by.add(current_user)
        # Increment points field by respective amount
        current_user.points += completedTask.points
        current_user.save()

    else:
        if current_user.student_tasks_completed < 2 and not completedTask.created_by == current_user:
            # Add user to completed by field in database
            completedTask.completed_by.add(current_user)
            # Increment points field by respective amount
            current_user.points += completedTask.points
            current_user.student_tasks_completed += 1
            current_user.next_possible_complete = datetime.date.today() + datetime.timedelta(days=1)
            current_user.save()

    current, total = completedTask.get_number_completed_task()
    if current == total:
        completers = completedTask.completed_by.all()
        for completer in completers:
            completer.points += 2
            completer.save()

    return redirect('/view_tasks')


# Isabel: 18/2/21
@login_required(login_url='/')
def table_chat(request, pk):
    # deal with if the requested table doesn't exist
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
    # get the tasks for the table - new: only notified of tasks set in last 24h
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    tasks = Task.objects.filter(table_id=table,
                                task_date__gte=date_from).order_by('task_date')
    # get all the users in the table
    users = table.coffeeuser_set.all()
    # see if currently studying
    users_studying = []
    other_users = []
    for user in users:
        if user.studying_until:
            # if the user set a time to study until
            if user.studying_until <= datetime.datetime.now():
                # they are not studying anymore
                user.studying_until = None
                user.save()
                other_users.append(user)
            else:
                users_studying.append(user)
        else:
            other_users.append(user)
    users_studying = sorted(users_studying, key=attrgetter("studying_until"),
                            reverse=True)
    # final
    context = {
        "table": table,
        "form": form,
        "messages": messages,
        "users_studying": users_studying,
        "other_users": other_users,
        "tasks": tasks,
        'users': CoffeeUser.objects.all(),
        'num_users': get_number_current_users()
    }
    return render(request, "table_chat.html", context)


def upvote(request, pk):
    current_user = request.user
    message = Message.objects.get(id=pk)
    if current_user not in message.message_upvote.all():
        message.message_upvote.add(current_user)
        message.total_upvotes += 1
        message.save()

    current_table = message.table_id.id
    return redirect('table_chat', pk=current_table)


# will and izzy
@login_required(login_url='/')
def edit_info(request):
    user = request.user

    if user.is_staff:
        if request.method == 'POST':
            form = CUserEditFormStaff(request.POST)
            if form.is_valid():
                # save what is entered and validate
                if form.cleaned_data['first_name']:
                    user.first_name = form.cleaned_data['first_name']

                if form.cleaned_data['last_name']:
                    user.last_name = form.cleaned_data['last_name']

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

                user.save()
                form = CUserEditFormStaff()
        else:
            form = CUserEditFormStaff()

    else:  # student user
        if request.method == 'POST':
            form = CUserEditForm(request.POST)
            if form.is_valid():
                # save what is entered and validate
                if form.cleaned_data['first_name']:
                    user.first_name = form.cleaned_data['first_name']

                if form.cleaned_data['last_name']:
                    user.last_name = form.cleaned_data['last_name']

                if form.cleaned_data['facebook_link']:
                    if form.cleaned_data['facebook_link'] == "/":
                        user.facebook = None
                    # facebook does not have a defined username for the link format
                    # like the others.
                    # here we check that the link is an actual facebook link
                    # not a random malicious link
                    elif form.cleaned_data['facebook_link'].startswith("https://www.facebook.com/"):
                        user.facebook = form.cleaned_data['facebook_link']

                if form.cleaned_data['instagram_username']:
                    if form.cleaned_data['instagram_username'] == "/":
                        user.instagram = None
                    else:
                        user.instagram = "https://www.instagram.com/" + \
                                            form.cleaned_data['instagram_username']

                if form.cleaned_data['twitter_handle']:
                    if form.cleaned_data['twitter_handle'] == "/":
                        user.twitter = None
                    else:
                        user.twitter = "https://twitter.com/" + \
                                            form.cleaned_data['twitter_handle']

                if form.cleaned_data['share_tables']:
                    if form.cleaned_data['share_tables'] == 'Yes':
                        user.share_tables = True
                    if form.cleaned_data['share_tables'] == 'No':
                        user.share_tables = False

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
        'tables': tables,
        'num_users': get_number_current_users()
    }
    return render(request, "edit_info.html", context)


# izzy 5/3/21
@login_required(login_url='/')
def profile_page(request, pk):
    # deal with if the requested user doesn't exist
    try:
        viewing_user = CoffeeUser.objects.get(id=pk)
    except CoffeeUser.DoesNotExist:
        return redirect('/handler404')

    context = {
        'year_entered': False,
        'course_entered': False,
        'num_users': get_number_current_users()
    }
    viewing_user = CoffeeUser.objects.get(id=pk)
    context['user'] = viewing_user
    if viewing_user.course:
        context['course_entered'] = True
    if viewing_user.year:
        context['year_entered'] = True

    # Student users can decide to share tables or not
    if viewing_user.share_tables and viewing_user.is_staff is not True:
        # get names of the tables the user is part of
        tables = viewing_user.cafe_table_ids.values_list('table_id', flat=True)
        # filter out the course table if it exists
        tables = filter(lambda x: x.startswith("COURSE: ") is not True, tables)
    else:
        tables = []
    context['tables'] = tables

    # get their collectables, if student
    collectables = []

    if viewing_user.is_staff is not True:
        pointsLevel = check_points_treshold(viewing_user.points)
        for i in range(int(pointsLevel)+1):
            collectables.append(list_coffee_link[i])

    context['collectable_pictures'] = collectables

    return render(request, "profile_page.html", context)


@login_required(login_url='/')
def report(request):
    user = request.user
    form = ReportForm()
    tables = CafeTable.objects.filter(
        university=user.university,
        table_id__in=user.cafe_table_ids.values_list('table_id', flat=True))
    form.fields['table_id'].queryset = tables

    context = {'form': form, 'num_users': get_number_current_users()}
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            detail = form.cleaned_data.get('detail')
            table_id = form.cleaned_data.get('table_id')

            report = Report.objects.create(
                title=title,
                category=category,
                detail=detail,
                table_id=table_id,
                flagged_by=user,
            )
            redirect('dashboard')
    return render(request, 'report.html', context)


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
