from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from api.views import MovieViewSet, CommentViewSet
from . import views

router = DefaultRouter()
router.register(r'movies', MovieViewSet, base_name='movies')
router.register(r'comments', CommentViewSet, base_name='comments')

urlpatterns = router.urls