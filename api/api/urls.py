from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet

router = DefaultRouter()
router.register('post', PostViewSet, base_name='post')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('users.urls')),

    # API
    path('v1/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
