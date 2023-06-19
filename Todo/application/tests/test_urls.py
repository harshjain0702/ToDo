from django.test import SimpleTestCase
from application.views import TaskList, TaskDelete, TaskUpdate, TaskDetail, TaskCreate
from django.urls import reverse, resolve, reverse_lazy


class TestUrls(SimpleTestCase):

    def test_task_url_is_resolved(self):
        url = reverse('tasks')
        self.assertEquals(resolve(url).func.view_class, TaskList)

    def test_task_create_url_is_resolved(self):
        url = reverse('task-create')
        self.assertEquals(resolve(url).func.view_class, TaskCreate)

    def test_task_detail_url_is_resolved(self):
        url = reverse('task', kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, TaskDetail)

    def test_task_update_url_is_resolved(self):
        url = reverse('task-update', kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, TaskUpdate)

    def test_task_delete_url_is_resolved(self):
        url = reverse('task-delete', kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, TaskDelete)
