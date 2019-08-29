from django.forms import ModelForm

from to_do_list.models import Task

class AddTaskForm(ModelForm):
    model = Task
    fields = ['name', 'deadline_date', 'description']
