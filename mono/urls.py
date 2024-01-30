from django.contrib import admin
from django.urls import path, include, re_path
from mono import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/', include(('app.urls', 'api'), namespace='api'), name='api'),
    
]

urlpatterns += i18n_patterns(
    re_path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard'), name='dashboard'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)