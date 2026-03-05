from django.urls import path
from .views import MediaView

urlpatterns = [
    path('', MediaView.as_view(), name='media-files'),
    path('<int:id>', MediaView.as_view()),
]
