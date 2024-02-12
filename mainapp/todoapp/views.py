from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'index.html')

def generate_todo_html(todo):
    return f"""
    <div id="todo-{todo.id}">
        <strong>{todo.title}</strong> - <em class="tag">{todo.status}</em>
        <p>{todo.description}</p>
        <button hx-get="/todos/{todo.id}/edit" hx-target="#editModal" hx-swap="outerHTML">Edit</button>
        <button hx-delete="/todos/{todo.id}/" hx-target="#todo-{todo.id}" hx-swap="outerHTML" hx-confirm="Are you sure you want to delete this todo?">Delete</button>
    </div>
    """


class TodoView(APIView):
    def get(self, request, format=None):
        todos = Todo.objects.all()

        items_html = ''.join([generate_todo_html(todo) for todo in todos])
        return HttpResponse(items_html)

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            saved_todo = serializer.save()

            return HttpResponse(generate_todo_html(saved_todo), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    def get_object(self, id):
        try:
            return Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        todo = self.get_object(id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            saved_todo = serializer.save()
            return HttpResponse(generate_todo_html(saved_todo))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        todo = self.get_object(id)
        todo.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
def edit_todo_form(request, id):
    todo = get_object_or_404(Todo, pk=id)

    form_html = f"""
    <div id="modalOverlay"></div>
    <div id="editModal">
        <form hx-post="/todos/{todo.id}/update" hx-target="#todo-{todo.id}" hx-swap="outerHTML">
            <input type="text" name="title" value="{todo.title}" required />
            <textarea name="description">{todo.description}</textarea>
            <button type="submit">Save Changes</button>
        <button hx-get="/todos/{todo.id}/cancel_edit" hx-target="#editModal">Close</button>
        </form>
    </div>
    """
    return HttpResponse(form_html)
