from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import RatesAPIView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  HomeView.as_view(), name='home'),
    path('api/rates/', RatesAPIView.as_view(), name='rates'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
