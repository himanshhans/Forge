from django.urls import path

from .views import AvatarGenerateView, AvatarUploadView

urlpatterns = [
    path("assets/avatar/upload/", AvatarUploadView.as_view(), name="avatar-upload"),
    path("assets/avatar/generate/", AvatarGenerateView.as_view(), name="avatar-generate"),
]
