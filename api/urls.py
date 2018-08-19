from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from api.views import MovieViewSet
from . import views

router = DefaultRouter()
router.register(r'movies', MovieViewSet, base_name='movies')

urlpatterns = [
]

urlpatterns += router.urls