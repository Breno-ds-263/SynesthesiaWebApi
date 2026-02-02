from django.urls import path
from .views import MediaView

urlpatterns = [
    path('files/', MediaView.as_view(), name='media-files'),
    path('files/<int:id>/', MediaView.as_view()),
]
