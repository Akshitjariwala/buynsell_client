from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('bands/',include('bands.urls')),
    path('admin/',admin.site.urls)
]

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


