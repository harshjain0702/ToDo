from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name = 'application/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse_lazy('tasks')


class Register(FormView):
    template_name = 'application/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        else:
            return super(Register, self).get(*args, **kwargs)


class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "application/task_list.html"
    context_object_name = 'tasks'
    paginate_by = 2
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = ""
        if self.request.GET:
            query = self.request.GET.get('q', '')
            context['query'] = str(query)
        # context['tasks'] = context['tasks'].filter(user=self.request.user)
        tasks_list = Task.objects.filter(user_id=self.request.user.id, title__icontains=query).only('title')

        page = self.request.GET.get('page', 1)
        tasks_list_paginator = self.paginator_class(tasks_list, self.paginate_by)
        try:
            tasks_list = tasks_list_paginator.page(page)
        except PageNotAnInteger:
            tasks_list = tasks_list_paginator.page(1)
        except EmptyPage:
            tasks_list = tasks_list_paginator.page(1)

        context['tasks'] = tasks_list
        return context


class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'application/task.html'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'is_completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'is_completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate, self).form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    context_object = 'task'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        try:
            task = Task.objects.get(pk=self.get_object().pk)
        except Task.DoesNotExist:
            self.template_name = 'application/error.html'
        return super().get_context_data(**kwargs)

    def test_func(self):
        task = self.get_object()

        if self.request.user == task.user:
            return True
        return False
