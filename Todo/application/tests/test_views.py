from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from application.models import Task
import json


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        task = Task.objects.create(user=self.user, title='test')

    def test_task_list_GET(self):
        client = Client()
        client.login(username='john', password='johnpassword')

        response = client.get(reverse_lazy('tasks'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('application/task_list.html')

    def test_task_detail_GET(self):
        client = Client()
        client.login(username='john', password='johnpassword')

        response = client.get(reverse('task', kwargs={"pk": 1}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('application/task.html')

    def test_task_update_GET(self):
        client = Client()
        client.login(username='john', password='johnpassword')

        response = client.get(reverse('task-update', kwargs={"pk": 1}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('application/task_form.html')

    def test_task_delete_GET(self):
        client = Client()
        client.login(username='john', password='johnpassword')

        response = client.get(reverse('task-delete', kwargs={"pk": 1}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('application/task_confirm_delete.html')

    def test_task_create_GET(self):
        client = Client()
        client.login(username='john', password='johnpassword')

        response = client.get(reverse('task-create'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('application/task_form.html')