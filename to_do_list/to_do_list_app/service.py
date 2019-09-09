from to_do_list_app.models import Task, FINISHED_TASK, NEW_TASK

class ToDoService:
    SUCCESS_CREATION_MESSAGE = 'Nowy Task został dodany'
    FAILED_CREATION_MESSAGE = 'Wypełnij poprawnie wszystkie pola'

    def __init__(self, user):
        self.user = user

    def add_new_task(self, validated_form):
        task = validated_form.save(commit=False)
        task.user = self.user
        task.save()

    def delete_task(self, task_id):
        task = Task.objects.get(id=task_id)
        if self.user.id == task.user_id:
            task.delete()

    def set_status_done(self, task_id):
        done_status_task = Task.objects.get(id=task_id)
        if self.user.id == done_status_task.user_id:
            done_status_task.status = FINISHED_TASK
            done_status_task.save()

    def set_status_new(self, task_id):
        new_status_task = Task.objects.get(id=task_id)
        if self.user.id == new_status_task.user_id:
            new_status_task.status = NEW_TASK
            new_status_task.save()

