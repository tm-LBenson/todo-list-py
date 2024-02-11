from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from todo_app.models import Todo



@login_required
def index(request):
    context = {'todos': Todo.objects.filter(user=request.user)}
    return render(request, 'index.html', context)

