from django.db import models
from django.contrib.auth.models import User

FINISHED_TASK = 2
NEW_TASK = 1
STATUS = (
    (NEW_TASK, "New"),
    (FINISHED_TASK, "Done")
)


class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=STATUS, default=NEW_TASK)
    deadline_date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)





