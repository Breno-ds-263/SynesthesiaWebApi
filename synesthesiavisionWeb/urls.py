from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ApiSyn/auth/', include('users.urls')),
    path('ApiSyn/media', include('media.urls')),
    path('ApiSyn/new', include('news.urls')),
    path('ApiSyn/materials', include('materials.urls')),
    path('ApiSyn/videos', include('video.urls')),
    path('ApiSyn/card', include('cards.urls')),
    path('ApiSyn/events', include('events.urls')),
    path('ApiSyn/articles', include('article.urls'))
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )