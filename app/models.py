from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Isabel & Victoria - 16/2/21, Isabel 17/2/21


class CafeTable(models.Model):
    # please note Django implicitly gives an auto incrementing primary
    # key field id = models.AutoField(primary_key=True)
    table_id = models.CharField(max_length=50)
    university = models.CharField(max_length=50)

    def __str__(self):
        return self.university + ":" + self.table_id


# required for custom user model
class CoffeeUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, university, is_staff,
                    password=None):
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
    is_staff = models.BooleanField(default=False)
    year = models.PositiveIntegerField(null=True, blank=True)
    course = models.CharField(max_length=50, blank=True)
    avatar_url = models.FilePathField(path="/img")
    cafe_table_ids = models.ManyToManyField(CafeTable, blank=True)
    points = models.PositiveIntegerField(default=0)
    studying_until = models.DateTimeField(null=True, blank=True)
    tasks_set_today = models.PositiveIntegerField(default=0)
    next_possible_set = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"  # users log in using their email
    REQUIRED_FIELDS = ["first_name", "last_name", "university", "is_staff"]

    objects = CoffeeUserManager()

    # Required functions for custom user model
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Task(models.Model):
    POINTS = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"),
              (10, "10"), (15, "15"), (20, "20"), (25, "25"), (30, "30"))
    # please note Django implicitly gives an auto incrementing primary
    # key field id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    table_id = models.ForeignKey(CafeTable, related_name="tasks",
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(CoffeeUser, related_name="created_tasks",
                                   on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(CoffeeUser, blank=True)
    # is task date date to be completed by or date set?
    task_date = models.DateTimeField(auto_now_add=True)
    task_content = models.TextField(max_length=4000)
    points = models.PositiveIntegerField(default=0, choices=POINTS)

    def __str__(self):
        return self.task_id


class Message(models.Model):
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
