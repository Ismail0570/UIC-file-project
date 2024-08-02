from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, FolderViewSet, FileShareAPIView

router = DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'folders', FolderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('file-share/', FileShareAPIView.as_view(), name='register')
]