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

def close_model(request):
    return HttpResponse('<div hx-trigger="load" hx-target="#modalOverlay" hx-swap="outerHTML" hx-get="todos/close-overlay" style="display: none" id="editModal"></div>')

def remove_overlay(request):
    return HttpResponse("<div></div>")

def update_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    serializer = TodoSerializer(todo, data=request.POST)
    if serializer.is_valid():
        saved_todo = serializer.save()
        return HttpResponse(generate_todo_html(saved_todo, request))
    return HttpResponse(serializer.errors, status=400)

def list_todos(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        items_html = ''.join([generate_todo_html(todo, request) for todo in todos])
        return HttpResponse(items_html)

def todo_detail(request, id):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, pk=id)
        return HttpResponse(generate_todo_html(todo, request))

def delete_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    todo.delete()
    return HttpResponse("")

def update_status(request, id):
    todo = get_object_or_404(Todo, pk=id)
    if todo.status == 'pending':
        todo.status = 'complete'
    else:
        todo.status = 'pending'
    todo.save()
    return HttpResponse(f'<span style="cursor: pointer" hx-trigger="click" hx-swap="outerHTML" hx-get="/todos/{todo.id}/status" class="tag"><em>{todo.status}</em></span>')
def getToken(request):
    csrf_token = get_token(request)
    token_element = f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">'
    return HttpResponse(token_element)

def create_todo(request):
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.POST)
        if serializer.is_valid():
            saved_todo = serializer.save()
            return HttpResponse(generate_todo_html(saved_todo, request), status=201)
        else:
            return HttpResponse(serializer.errors, status=400)

def generate_todo_html(todo, request):
    csrf_token = get_token(request)
    return f"""
    <div id="todo-{todo.id}">
        <strong>{todo.title}</strong> - <span style="cursor: pointer" hx-trigger="click" hx-swap="outerHTML" hx-get="/todos/{todo.id}/status" class="tag"><em>{todo.status}</em></span>
        <p>{todo.description}</p>
        <button hx-get="/todos/{todo.id}/edit" hx-target="#editModal" hx-swap="outerHTML">Edit</button>
        <form id="delete-todo-{todo.id}" action="/todos/{todo.id}/delete" method="post" style="display: inline;">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <button type="submit" form="delete-todo-{todo.id}" hx-post="/todos/{todo.id}/delete" hx-target="#todo-{todo.id}" hx-swap="outerHTML" hx-confirm="Are you sure you want to delete this todo?">Delete</button>
        </form>
        <script id="reset">
            document.getElementById('addTodoForm').reset();
            document.getElementById('reset').remove();
        </script>
    </div>
    """

def edit_todo_form(request, id):
    todo = get_object_or_404(Todo, pk=id)
    csrf_token = get_token(request)
    form_html = f"""
    <div id="modalOverlay"></div>
    <div id="editModal">
        <form hx-post="/todos/{todo.id}/update" hx-target="#todo-{todo.id}" hx-swap="outerHTML">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <input type="text" name="title" value="{todo.title}" required />
            <textarea name="description">{todo.description}</textarea>
            <button hx-target="#editModal" hx-swap="outerHTML" type="submit">Save Changes</button>
            <button hx-swap="outerHTML" hx-get="/todos/cancel_edit" hx-target="#editModal">Close</button>
        </form>
    </div>
    """
    return HttpResponse(form_html)
