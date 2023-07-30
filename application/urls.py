from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, Register
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('login/', csrf_exempt(CustomLoginView.as_view()), name='login'),
    path('register/', csrf_exempt(Register.as_view()), name='register'),
    path('logout/', csrf_exempt(LogoutView.as_view(next_page='login')), name='logout'),
    path('', csrf_exempt(TaskList.as_view()), name='tasks'),
    path('task/<int:pk>/', csrf_exempt(TaskDetail.as_view()), name='task'),
    path('create-task/', csrf_exempt(TaskCreate.as_view()), name='task-create'),
    path('task-update/<int:pk>/', csrf_exempt(TaskUpdate.as_view()), name='task-update'),
    path('task-delete/<int:pk>/', csrf_exempt(TaskDelete.as_view()), name='task-delete'),
]
