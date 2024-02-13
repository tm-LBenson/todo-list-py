from django.http import HttpResponse
from django.shortcuts import render
from .models import Todo
from .serializers import TodoSerializer
from django.shortcuts import get_object_or_404
from django.views import View
from django.middleware.csrf import get_token

def home(request):
    return render(request, 'index.html')
from django.http import HttpResponse
from django.middleware.csrf import get_token



def update_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    serializer = TodoSerializer(todo, data=request.POST)
    if serializer.is_valid():
        saved_todo = serializer.save()
        return HttpResponse(generate_todo_html(saved_todo))
    return HttpResponse(serializer.errors, status=400)

def list_todos(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        items_html = ''.join([generate_todo_html(todo) for todo in todos])
        return HttpResponse(items_html)

def create_todo(request):
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.POST)
        if serializer.is_valid():
            saved_todo = serializer.save()
            return HttpResponse(generate_todo_html(saved_todo), status=201)
        else:
            return HttpResponse(serializer.errors, status=400)

def todo_detail(request, id):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, pk=id)
        return HttpResponse(generate_todo_html(todo))

def delete_todo(request, id):
    if request.method == 'DELETE':
        todo = get_object_or_404(Todo, pk=id)
        todo.delete()
        return HttpResponse(status=204)
    
def generate_todo_html(todo):
    return f"""
    <div id="todo-{todo.id}">
        <strong>{todo.title}</strong> - <em class="tag">{todo.status}</em>
        <p>{todo.description}</p>
        <button hx-get="/todos/{todo.id}/edit" hx-target="#editModal" hx-swap="outerHTML">Edit</button>
        <button hx-delete="/todos/{todo.id}/" hx-target="#todo-{todo.id}" hx-swap="outerHTML" hx-confirm="Are you sure you want to delete this todo?">Delete</button>
    </div>
    """

def edit_todo_form(request, id):
    todo = get_object_or_404(Todo, pk=id)
    csrf_token = get_token(request)
    form_html = f"""
    <div id="modalOverlay"></div>
    <div id="editModal">
        <form hx-post="/todos/{todo.id}/update" hx-target="#todo-{todo.id}" hx-swap="outerHTML">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}" />
            <input type="text" name="title" value="{todo.title}" required />
            <textarea name="description">{todo.description}</textarea>
            <button type="submit">Save Changes</button>
        <button hx-get="/todos/{todo.id}/cancel_edit" hx-target="#editModal">Close</button>
        </form>
    </div>
    """
    return HttpResponse(form_html)
