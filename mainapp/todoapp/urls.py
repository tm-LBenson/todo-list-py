from django.urls import path
from .views import Todo

urlpatterns = [
    path('todo/', Todo.as_view(), name='todos'),
]