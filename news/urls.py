from django.urls import path
from .views import NewsView

urlpatterns = [
    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:id>', NewsView.as_view(), name='news-detail'),
]
