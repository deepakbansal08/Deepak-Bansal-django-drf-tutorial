from django.urls import path
from projects.views import ProjectMemberApiViewSet

app_name = 'projects'

from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'projects', ProjectMemberApiViewSet, 'projects')

urlpatterns = router.urls
