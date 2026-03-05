from django.urls import path

from video.views import VideoView

urlpatterns = [
    path('', VideoView.as_view(), name='videos'),
    path('/<int:id>', VideoView.as_view(), name='videos-detail'),
]