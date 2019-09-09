from django.forms import ModelForm, SelectDateWidget

from to_do_list_app.models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'deadline_date', 'description']
        widgets = {'deadline_date':SelectDateWidget()}