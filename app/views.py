""" Functions called when navigating to a specific page in the web app """

from __future__ import unicode_literals
from operator import attrgetter
import datetime
import pytz
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from app.forms import SignUpForm, LoginForm, PostMessageForm, CUserEditForm, \
                   CreateTaskForm, StudyBreaksForm, CUserEditFormStaff, \
                   ReportForm
from app.models import CoffeeUser, CafeTable, Message, Task, Report, \
                       Notification
from app.small_scripts_def import check_points_treshold, how_much_to_go


list_coffee_link = ["images/espresso.PNG", "images/americano.PNG",
                    "images/cappuccino.PNG", "images/hot_chocolate.PNG",
                    "images/latte.PNG", "images/mocha.PNG",
                    "images/matcha.PNG", "images/frappuccino.PNG",
                    "images/ice_tea.PNG", "images/bubble_tea.PNG"]
list_coffee_name = ["Espresso", "Americano", "Cappuccino", "Hot Chocolate",
                    "Latte", "Mocha", "Matcha Latte", "Frappuccino",
                    "Iced Tea", "Bubble Tea"]


# Isabel 3/3/21
def get_number_current_users():
    """ Calculates the number of active users

    Returns:
        active::int
            The number of users currently using the web app
    """
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
    """ Retrieves all messages in a specific table and renders them

    Args:
        request::HttpRequest
            Object that contains metadata about the request
        table::int
            The id of the table where the specific messages are written

    Returns:
        render::HttpResponse
            Renders the 'messages.html' file and passes the retireved messages
            as a parameter
    """
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

    # get the 100 most recent messages in the table
    messages = Message.objects.filter(table_id=table).order_by(
                'message_date')[:100]

    # format the times so they can be processed in JS for timezone conversion
    for msg in messages:
        msg.message_date = pytz.utc.localize(msg.message_date).isoformat()
    return render(request, 'messages.html', {'messages': messages})


def check_recurring_tasks():
    """ Checks whether a reccuring task exists and removes it if found """
    # get recurring tasks that still must be repeated
    recurring_tasks = Task.objects.exclude(max_repeats=0).exclude(
        recurrence_interval="n")
    for task in recurring_tasks:
        # set the task again if necessary
        if task.recurring_date == datetime.date.today() and \
          task.no_of_repeats <= task.max_repeats:
            task.completed_by.remove(*task.completed_by.all())
            task.no_of_repeats += 1
            task.date_set = datetime.date.today()
            task.save()


# Victoria: 18/2/21
def index(request):
    """ Checks to see whether login credentials are valid and logs user in if
        they are

    Args:
        request::HttpRequest
            Object that contains metadata about the request

    Returns:
        redirect::HttpResponse
            Redirects user 'table_view.html' if login credentials are valid
        render::HttpResponse
            Renders the 'login.html' page and passes the login form as a
            parameter

    """
    context = {}

    # if user is already authenticated they will be redirected to home
    # whenever they try to access /login until they logout
    user = request.user
    if user.is_authenticated:
        return redirect('table_view')

    # validate and login user when credentials submitted
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # fixing a weird error if email format last part 1 char
        if len(request.POST['email'].split(".")[-1]) > 1:
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('table_view')

    # provide form for user to enter credentials
    context['login_form'] = LoginForm()

    return render(request, 'login.html', context)


# Victoria: 18/2/21
def log_out(request):
    """ Logs out the user

    Args:
        request::HttpRequest
            Object that contains metadata about the request
    Returns:
        redirect::HttpResponse
            Redirects user to the login page
    """
    logout(request)
    return redirect('/')


# Isabel: 18/2/21
def signup(request):
    """ Checks whether sign up form is valid and gathers user information
        If users has already signed up, he gets logged in

    Args:
        request::HttpRequest
            Object that contains metadata about the request

    Returns:
        render::HttpResponse
            Renders the 'sign_up.html' file and passes as a context parameter
            the sign up form
    """
    context = {}
    if request.method == 'POST':
        # validate the form
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid() and form.cleaned_data.get('accept_terms'):
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            # log in the newly created user
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
    """ Finds all the tables for which the given user is part of
        and displays them

    Args:
        request::HttpRequest
            Object that contains metadata about the request

    Returns:
        render::HttpResponse
            Renders the 'table_view.html' file and passes as a parameter the
            tables which the logged-in user is part of along with the number
            of active users.
    """
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
    """ Fetches and displays all relevant information for the dashboard

    Args:
        request::HttpRequest
            Object that contains metadata about the request

    Returns:
        renders::HttpResponse
            Renders the 'dashboard.html' page and passes all relevant
            information as a parameter inside the contexts
    """
    user = request.user

    # the tables the user is part of
    tables = CafeTable.objects.filter(
        university=user.university,
        table_id__in=user.cafe_table_ids.values_list('table_id',
                                                     flat=True)
    )

    # Get last 10 notifications pertaining to the user
    notifications = Notification.objects.filter(table_id__in=tables)[:9]
    # format the times so they can be processed in JS for timezone conversion
    for notif in notifications:
        notif.date = pytz.utc.localize(notif.date).isoformat()

    # 10 highest scoring students for the leaderboard
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

        # Collectables:

        # this derives an int from the points earned by the user,
        # the int corresponds to the name of the collectable's picture in the
        # files it then concatenates together: the int returned and the link to
        # the image which in the end gives a link to the collectable's image
        # corresponding to the number of points
        current_user_points = user.points
        points_level = check_points_treshold(current_user_points)
        # getting the name from the list_coffee with the index for the current
        # max collectable
        link_img = list_coffee_link[int(points_level)]
        name_coffee = list_coffee_name[int(points_level)]

        # creating the list for the previous collectables
        previous_collectables = []
        index_list = 0
        while index_list < int(points_level):
            previous_collectables.append(list_coffee_link[index_list])
            index_list += 1

        # calculating how many points to reach next collectable
        points_to_go_next_collectable = int(how_much_to_go(points_level))

        # Notification for points left
        if points_to_go_next_collectable < 10:
            n_text = user.first_name + \
                " has less than 10 points to go until their next award!"
            notif = Notification(table_id=0, notification_type=1,
                                 text_preview=n_text)
            notif.save()

        # see if the student is currently studying
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

    # see if user can set tasks
    can_set_tasks = True
    if user.tasks_set_today >= 2 and not user.is_staff and \
       user.next_possible_set > datetime.date.today():
        can_set_tasks = False

    # format date joined so that it can be processed by JS for correct timezone
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
        'can_set_tasks': can_set_tasks,
        'notifications': notifications,
    }
    return render(request, "dashboard.html", context)


# Victoria 04 & 05/03/21
@login_required(login_url="/")
def set_tasks(request):
    """ Retrives the information from the set_tasks page form
        and creates a task for the given table. Checks for the number
        of tasks that have already been created are also made.

    Args:
        request::HttpRequest
            Object that contains metadata about the request

    Returns:
        render::HttpResponse
            Renders the 'set_tasks.html' page and passes the set tasks form as
            context
    """
    user = request.user
    form = CreateTaskForm(user=request.user)

    # Users can only set tasks for tables they are part of
    tables = CafeTable.objects.filter(
        university=user.university,
        table_id__in=user.cafe_table_ids.values_list('table_id', flat=True))
    form.fields['table_id'].queryset = tables

    # reset number of tasks set today if necessary
    if user.tasks_set_today >= 2 and \
       user.next_possible_set == datetime.date.today():
        user.tasks_set_today = 0
        user.save()

    # students can set max 2 tasks per day (to avoid spamming)
    if user.tasks_set_today >= 2 and not user.is_staff:
        return redirect("dashboard")

    context = {'form': form, 'num_users': get_number_current_users()}

    if request.method == 'POST':
        # create task with provided data
        form = CreateTaskForm(request.POST, user=request.user)
        if form.is_valid():
            task_name = form.cleaned_data.get('task_name')
            table_id = form.cleaned_data.get('table_id')
            task_content = form.cleaned_data.get('task_content')
            points = form.cleaned_data.get('points')
            recurrence_interval = form.cleaned_data.get('recurrence_interval')
            max_repeats = form.cleaned_data.get('max_repeats')
            Task.objects.create(  # removed task =
                task_name=task_name,
                created_by=user,
                table_id=table_id,
                task_content=task_content,
                points=points,
                recurrence_interval=recurrence_interval,
                max_repeats=max_repeats
            )
            user.tasks_set_today += 1
            user.save()

            # Add notification
            task_text = user.first_name + " has added " + task_name + \
                " as a new task! Check it out!"
            notification = Notification(table_id=table_id, notification_type=3,
                                        text_preview=task_text)
            notification.save()

            # if student, redirect if can't set more tasks now
            if user.tasks_set_today >= 2 and not user.is_staff:
                user.next_possible_set = datetime.date.today() + \
                    datetime.timedelta(days=1)
                user.save()
                return redirect("dashboard")

        else:
            context["CreateTaskForm"] = form
    else:
        context["CreateTaskForm"] = form

    # by default, tasks are not recurring
    form.fields['recurrence_interval'].initial = "n"
    return render(request, 'set_tasks.html', context)


# Alex, Isabel & Victoria 20/2/21
@login_required(login_url="/")
def view_tasks(request):
    """ Displays all the tasks that have been set for the current user
        and which haven't already been completed by him/her.

    Args:
        request::HttpRequest
            Object that contains metadata about the request.
    Returns:
        render::HttpResponse
            Renders the 'view_tasks.html' page and passes as a parameter
            the required tasks, active users and all other users.
    """
    current_user = request.user

    # only students can view and complete tasks
    if current_user.is_staff:
        return redirect("dashboard")

    # get the tables the current user is part of
    tables = CafeTable.objects.filter(
        university=current_user.university,
        table_id__in=current_user.cafe_table_ids.values_list('table_id',
                                                             flat=True)
    )

    # check if any recurring tasks need to be set
    check_recurring_tasks()

    # get the tasks corresponding to the user's tables that they haven't done
    tasks = Task.objects.filter(table_id__in=tables).exclude(
        completed_by=current_user).exclude(created_by=current_user)

    # prepare number of people who completed a task and can complete a task
    # in format required by django html template
    if tasks:
        complete_current = []
        complete_total = []
        for task in tasks:
            current, total = task.get_number_completed_task()
            complete_current.append(current)
            complete_total.append(total)
        task_info = zip(tasks, complete_current, complete_total)
    else:
        task_info = []

    context = {
        'tasks': task_info,
        'users': CoffeeUser.objects.all(),
        'num_users': get_number_current_users()
    }
    return render(request, 'view_tasks.html', context)


# Victoria & Alex 05/03/21
@login_required(login_url='/')
def complete_task(request, pk):
    """ Marks task as completed and awards the user with the corresponding
        points. Checks are made to see how many tasks the current user has
        completed in the day to avoid spamming.
    Args:
        request::HttpRequest
            Object that contains metadata about the request.
        pk::int
            The id of the specific task for which the completed button was
            clicked
    Returns:
        redirect::HttpResponse
            redirects user to the 'view_tasks.html' page
    """
    # Get the current user logged in
    current_user = request.user

    # Get the task for which the button is pressed
    completed_task = Task.objects.get(pk=pk)

    # reset number of student tasks completed if necessary
    if current_user.student_tasks_completed >= 2 and \
       current_user.next_possible_complete == datetime.date.today():
        current_user.student_tasks_completed = 0
        current_user.save()

    # complete staff set task and earn points
    if completed_task.created_by.is_staff:
        # Add user to completed by field in database
        completed_task.completed_by.add(current_user)
        # Increment points field by respective amount
        current_user.points += completed_task.points
        current_user.save()

    else:
        # complete student set task and earn points if you can still complete
        # student set tasks today and you did not create this task
        if current_user.student_tasks_completed < 2 and not \
           completed_task.created_by == current_user:
            # Add user to completed by field in database
            completed_task.completed_by.add(current_user)
            # Increment points field by respective amount
            current_user.points += completed_task.points
            current_user.student_tasks_completed += 1
            current_user.next_possible_complete = datetime.date.today() + \
                datetime.timedelta(days=1)
            current_user.save()

    # bonus points if everyone (who can) completes the task
    current, total = completed_task.get_number_completed_task()
    if current == total:
        completers = completed_task.completed_by.all()
        for completer in completers:
            completer.points += 2
            completer.save()

    # recurring tasks
    if completed_task.recurrence_interval == "d":
        completed_task.recurring_date = completed_task.date_set + \
            datetime.timedelta(days=1)
    elif completed_task.recurrence_interval == "w":
        completed_task.recurring_date = completed_task.date_set + \
            datetime.timedelta(weeks=1)
    completed_task.save()

    # Make a notification about the completed task
    not_text = "Someone has completed " + \
        str(completed_task.task_name) + " and has earned " + \
        str(completed_task.points) + " points in doing so!"
    notification = Notification(table_id=completed_task.table_id,
                                notification_type=3, text_preview=not_text)
    notification.save()

    return redirect('/view_tasks')


# Isabel: 18/2/21
@login_required(login_url='/')
def table_chat(request, pk):
    """ Shows users the messages and tasks set for a specific table

    Args:
        request::HttpRequest
            Object that contains metadata about the request.
        pk::int
            The id of the specific table for which messages are displayed
            and tasks are set

    Returns:
        render::HttpResponse
            Renders the 'table_chat.html' page
    """
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
            Message.objects.create(  # removed msg =
                table_id=table,
                created_by=current_user,
                message_content=message_content,
            )
            form = PostMessageForm()
    else:
        form = PostMessageForm()

    # show the existing messages by querying db
    messages = Message.objects.filter(table_id=table).order_by(
                'message_date')[:100]

    # get the tasks for the table set today
    check_recurring_tasks()
    date_from = datetime.date.today()
    tasks = Task.objects.filter(table_id=table,
                                date_set=date_from)

    # get all the users in the table
    users = table.coffeeuser_set.all()

    # see if users are currently studying
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


# Alex 4/3/21
def upvote(request, pk):
    """ Increases the upvote count for specific message when
        upvote button is clicked.
    Args:
        request::HttpRequest
            Object that contains metadata about the request.
        pk::int
            The id of the message for which the upvote button is clicked.
    Returns:
        redirect::HttpResponse
            Redirects user to the 'table_chat.html' page and passes as a
            parameter the table id for which the liked message is part of
    """
    current_user = request.user
    message = Message.objects.get(id=pk)

    # upvote the message if that user hasn't already
    if current_user not in message.message_upvote.all():
        message.message_upvote.add(current_user)
        message.total_upvotes += 1
        message.save()

    current_table = message.table_id.id
    return redirect('table_chat', pk=current_table)


# will and izzy
@login_required(login_url='/')
def edit_info(request):
    """ Displays the edit info form. Collects all information from the edit
        info form and updates the respective fields with the new information.
        In addition, icons that redirect user to external social media are
        present.

    Args:
        request::HttpRequest
            Object that contains metadata about the request.
    Returns:
        render::HttpResponse
            Renders the 'edit_info.html' page

    """
    user = request.user

    if request.method == 'POST':
        # load the correct form for students/staff
        if user.is_staff:
            form = CUserEditFormStaff(request.POST)
        else:
            form = CUserEditForm(request.POST)

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
                    table = user.cafe_table_ids.get(
                        table_id=old_table_name)
                    user.cafe_table_ids.remove(table)

                new_course = form.cleaned_data['course'].lower()
                user.course = new_course
                # upper case throughout so not duplicates with different
                # casing
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
                # make lower again
                try:
                    table = user.cafe_table_ids.get(
                        table_id=table_name_to_rm)
                    user.cafe_table_ids.remove(table)
                except CafeTable.DoesNotExist:
                    pass

            if user.is_staff is False:
                if form.cleaned_data['facebook_link']:
                    if form.cleaned_data['facebook_link'] == "/":
                        # clear
                        user.facebook = None
                    # facebook does not have a defined username for the link
                    # format like the others.
                    # here we check that the link is an actual facebook link
                    # not a random malicious link
                    elif form.cleaned_data['facebook_link'].startswith(
                       "https://www.facebook.com/"):
                        user.facebook = form.cleaned_data['facebook_link']

                if form.cleaned_data['instagram_username']:
                    if form.cleaned_data['instagram_username'] == "/":
                        # clear
                        user.instagram = None
                    else:
                        user.instagram = "https://www.instagram.com/" + \
                            form.cleaned_data['instagram_username']

                if form.cleaned_data['twitter_handle']:
                    if form.cleaned_data['twitter_handle'] == "/":
                        # clear
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

            user.save()

    # load the correct form for students/staff
    if user.is_staff:
        form = CUserEditFormStaff()
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
    """ Displays all relevant information for a particular user

    Args:
        request::HttpRequest
            Object that contains metadata about the request.
        pk::int
            The id of the users profile page
    Returns:
        render::HttpResponse
            Renders the 'profile_page.html' page and passes as parameter
            all of the given users information
    """
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

    # see what information the user has set, to avoid errors if not set
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
        # filter out the course table if it exists (as already shown as course)
        tables = filter(lambda x: x.startswith("COURSE: ") is not True, tables)
    else:
        tables = []
    context['tables'] = tables

    # get their collectables, if student
    collectables = []
    if viewing_user.is_staff is not True:
        points_level = check_points_treshold(viewing_user.points)
        for i in range(int(points_level)+1):
            collectables.append(list_coffee_link[i])
    context['collectable_pictures'] = collectables

    return render(request, "profile_page.html", context)


# izzy 7/3/21
@login_required(login_url='/')
def reporting(request):
    """ Displays the report form that users can fill and submit

    Args:
        request::HttpRequest
            Object that contains metadata about the request.

    Returns:
        render::HttpResponse
            Renders the 'report.html' page
    """
    user = request.user
    form = ReportForm()
    # users can only report issues for tables they are part of
    tables = CafeTable.objects.filter(
        university=user.university,
        table_id__in=user.cafe_table_ids.values_list('table_id', flat=True))
    form.fields['table_id'].queryset = tables

    context = {'form': form, 'num_users': get_number_current_users()}
    if request.method == 'POST':
        # register the report so it can be accessed on admin view
        form = ReportForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            detail = form.cleaned_data.get('detail')
            table_id = form.cleaned_data.get('table_id')

            Report.objects.create(
                title=title,
                category=category,
                detail=detail,
                table_id=table_id,
                flagged_by=user,
            )
            redirect('dashboard')
    return render(request, 'report.html', context)


def health(request):
    """ Checks to see whether web application is running correctly (status) """
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    """ Manages any 404 errors """
    return render(request, '404.html', status=404)


def handler500(request):
    """ Manages any 500 errors """
    return render(request, '500.html', status=500)


def privacy(request):
    """ Renders the 'privacy.html' page """
    return render(request, 'privacy.html')


def terms(request):
    """ Renders the 'terms.html' page """
    return render(request, 'terms.html')
