from django.db import models
from django.contrib.auth.models import User

# Isabel & Victoria - 16/2/21

class CafeTable(models.Model):
    table_id = models.CharField(max_length=50)  # name of the table
    # members = models.ManyToManyField(CoffeeUser)


class CoffeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username, password, email, first_name, last_name included here
    university = models.CharField(max_length=50)
    role = models.CharField(max_length=10)
    year = models.PositiveIntegerField()
    course = models.CharField(max_length=50)
    avatar_url = models.FilePathField(path="/img")
    cafe_table_ids = models.ManyToManyField(CafeTable)
    points = models.PositiveIntegerField(default=0)


class Task(models.Model):
    task_id = models.PositiveIntegerField()
    table_id = models.ForeignKey(CafeTable, related_name="tasks",
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(CoffeeUser, related_name="created_tasks",
                                   on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(CoffeeUser)
    task_date = models.DateTimeField(auto_now_add=True)
    task_content = models.TextField(max_length=4000)
    points = models.PositiveIntegerField(default=0)


# 1st normal form redundant due to Django db implementation


class Message(models.Model):
    message_id = models.PositiveIntegerField()
    table_id = models.ForeignKey(CafeTable, related_name="messages",
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(CoffeeUser, related_name="messages",
                                   on_delete=models.CASCADE)
    message_date = models.DateTimeField(auto_now_add=True)
    message_content = models.TextField(max_length=4000)


# leaderboard class redundant - simply sort user table by points and only
# display top xxx people
