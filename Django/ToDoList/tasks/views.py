from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

# Create a form
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

Tasks = []

def index(request):
    return render(request, "tasks/index.html", {
        'tasks': Tasks
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            Tasks.append(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    else:
        form = NewTaskForm()

    return render(request, "tasks/add.html", {
        "form": form
    })

def delete(request):
    if request.method == "POST":
        indexes_to_delete = request.POST.getlist("tasks")
        indexes_to_delete = [int(index) for index in indexes_to_delete]
        for index in sorted(indexes_to_delete, reverse=True):
            if 0 <= index < len(Tasks):
                del Tasks[index]

    # Preprocess enumeration for the template
    enumerated_tasks = list(enumerate(Tasks))

    return render(request, "tasks/delete.html", {
        "tasks": enumerated_tasks
    })
