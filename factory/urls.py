from django.conf.urls import url
from django.urls import path

from rest_framework import routers

from .views import TasksView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tasks', TasksView, base_name='tasks')
urlpatterns = router.urls