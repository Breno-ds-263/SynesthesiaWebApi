from django.urls import path

from events.views import EventsView

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('/<int:id>', EventsView.as_view(), name='events-detail'),
]
