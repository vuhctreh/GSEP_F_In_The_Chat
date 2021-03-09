""" Classes for all objects that are used throughout the application """

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Isabel & Victoria - 16/2/21, Isabel 17/2/21


class CafeTable(models.Model):
    """ Contains the information for each table (group) """
    # please note Django implicitly gives an auto incrementing primary
    # key field id = models.AutoField(primary_key=True)
    table_id = models.CharField(max_length=50)
    university = models.CharField(max_length=50)

    def __str__(self):
        """ Function to return the id of a specific table

        Returns:
            self.table_id::int
                The id of the specific table
        """
        return self.table_id


# required for custom user model
class CoffeeUserManager(BaseUserManager):
    """ Class for creating either a normal user or a super user """

    def create_user(self, email, first_name, last_name, university, is_staff,
                    password=None):
        """ Creating a user without admin or superuser permissions

        Args:
            email::string
                Users email address
            first_name::string
                Users first name 
            last_name::string
                Users last name
            university::string
                Users inputted university
            is_staff::boolean
                Boolean value to confirm whether user is a staff member
            password::string
                User password

        Returns:
            user::CoffeeUserManager
                A coffee user object is returned
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must give their first name")
        if not last_name:
            raise ValueError("Users must give their last name")
        if not university:
            raise ValueError("Users must supply their University")
        if not is_staff:
            is_staff = False
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            university=university,
            is_staff=is_staff
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, university,
                         is_staff, password):
        """ Creating a user that also has admin and superuser permissions

        Args:
            email::string
                Users email address
            first_name::string
                Users first name 
            last_name::string
                Users last name
            university::string
                Users inputted university
            is_staff::boolean
                Boolean value to confirm whether user is a staff member
            password::string
                User password

        Returns:
            user::CoffeeUserManager
                A coffee user object is returned
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            university=university,
            is_staff=is_staff
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CoffeeUser(AbstractBaseUser):
    """ Contains all possible information for a user """

    AVAILABLE_UNIS = (
        ("University of Exeter", "University of Exeter"),
        ("Test uni", "Test uni")
    )

    email = models.EmailField(verbose_name="email", unique=True)
    # The following are required as extending AbstractBaseUser
    # and creating custom user model
    date_joined = models.DateTimeField(verbose_name="date_joined",
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    university = models.CharField(max_length=50, choices=AVAILABLE_UNIS)
    year = models.PositiveIntegerField(null=True, blank=True)
    course = models.CharField(max_length=50, blank=True)
    cafe_table_ids = models.ManyToManyField(CafeTable, blank=True)
    points = models.PositiveIntegerField(default=0)
    studying_until = models.DateTimeField(null=True, blank=True)
    share_tables = models.BooleanField(default=True)
    tasks_set_today = models.PositiveIntegerField(default=0)
    next_possible_set = models.DateField(null=True, blank=True)
    student_tasks_completed = models.PositiveIntegerField(default=0)
    next_possible_complete = models.DateField(null=True, blank=True)
    # Social media
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"  # users log in using their email
    REQUIRED_FIELDS = ["first_name", "last_name", "university", "is_staff"]

    objects = CoffeeUserManager()

    # Required functions for custom user model
    def __str__(self):
        """ Returns the specific users email address """
        return self.email

    def has_perm(self, perm, obj=None):
        """ Returns a boolean value depending on if user has admin permissions """
        return self.is_admin

    def has_module_perms(self, app_label):
        """ Returns a boolean value depending on if user has module permissions """
        return True


class Task(models.Model):
    """ Contains all fields for a task """
    POINTS = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"),
              (10, "10"), (15, "15"), (20, "20"), (25, "25"), (30, "30"))
    REPEATS = (("n", "NONE"), ("d", "DAILY"), ("w", "WEEKLY"))
    # please note Django implicitly gives an auto incrementing primary
    # key field id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    table_id = models.ForeignKey(CafeTable, related_name="tasks",
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(CoffeeUser, related_name="created_tasks",
                                   on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(CoffeeUser, blank=True)
    date_set = models.DateField(auto_now_add=True)
    task_content = models.TextField(max_length=4000)
    points = models.PositiveIntegerField(default=0, choices=POINTS)
    recurring_date = models.DateField(null=True, blank=True)
    recurrence_interval = models.CharField(max_length=1, choices=REPEATS)
    no_of_repeats = models.PositiveIntegerField(default=0)
    max_repeats = models.PositiveIntegerField(default=0)

    REQUIRED_FIELDS = ["task_name", "task_content"]

    def __str__(self):
        """ Returns the name of the specific task """
        return self.task_name

    def get_number_completed_task(self):
        """ Returns the number of users who've completed a specific task

        Returns:
            result::int
                Number of people who've completed task
        """
        out_of = self.table_id.coffeeuser_set.exclude(is_staff=1).count()
        if self.created_by.is_staff:
            result = (self.completed_by.count(), out_of)
        else:
            result = (self.completed_by.count(), out_of - 1)
        return result


class Message(models.Model):
    """ Contains all the information for a message """
    # please note Django implicitly gives an auto incrementing primary
    # key field id = models.AutoField(primary_key=True)
    table_id = models.ForeignKey(CafeTable, related_name="messages",
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(CoffeeUser, related_name="messages",
                                   on_delete=models.CASCADE)
    message_date = models.DateTimeField(auto_now_add=True)
    message_content = models.TextField(max_length=4000)
    message_upvote = models.ManyToManyField(CoffeeUser, related_name="message_upvote")
    total_upvotes = models.PositiveIntegerField(default=0)


class Report(models.Model):
    """ Contains all the information that a report may have """

    REPORT_CLASSES = (
        ("Table (general)", "Table (general)"),
        ("Task", "Task"),
        ("Messages", "Messages"),
        ("Other", "Other")
    )

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=REPORT_CLASSES)
    detail = models.CharField(max_length=250)
    table_id = models.ForeignKey(CafeTable, related_name="reports",
                                 on_delete=models.CASCADE)
    flagged_by = models.ForeignKey(CoffeeUser, related_name="reports",
                                   on_delete=models.CASCADE)


class Notification(models.Model):
    """ Contains the contents of a notification """
    NOTIFICATION_TYPES = ((1, 'Award'), (2, 'Points'), (3, 'Task'))

    table_id = models.ForeignKey(CafeTable, on_delete=models.CASCADE,
                                 related_name="noti_post", blank=False,
                                 null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
