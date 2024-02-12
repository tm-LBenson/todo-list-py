from django.urls import path
from .views import TodoView, TodoDetailView, home, edit_todo_form

urlpatterns = [
    path('todos/', TodoView.as_view(), name='todos'),
    path('todos/<int:id>/', TodoDetailView.as_view(),
    name='todo_detail'),
    path('todos/<int:id>/edit', edit_todo_form, name='edit_todo_form'),
    path('', home, name='home'),
]
