from django.conf.urls import url
from django.urls import path

from rest_framework import routers

from .views import TaskView, SessionView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tasks', TaskView, base_name='tasks')
router.register(r'sessions', SessionView, base_name='sessions')
urlpatterns = router.urls