from django.urls import path
from .views import CardView

urlpatterns = [
    path('', CardView.as_view(), name='cards'),
    path('/<int:id>', CardView.as_view(), name='cards-detail'),
]
