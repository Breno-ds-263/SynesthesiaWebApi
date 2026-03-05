from django.urls import path
from .views import NewsView

urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('/<int:id>', NewsView.as_view(), name='news-detail'),
]
