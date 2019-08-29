from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (1, "New"),
    (2, "Done")
)

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=STATUS, default=1)
    deadline_date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
