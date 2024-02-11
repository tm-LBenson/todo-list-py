from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoItemViewSet
from todo_api.views import index
router = DefaultRouter()
router.register(r'todos', TodoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', index, name='index'),
]
