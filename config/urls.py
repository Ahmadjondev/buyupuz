from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/v3/', include('manager.urls')),
                  path('v3/', include('user.urls')),
                  path('v3/', include('app.urls')),
                  path('v3/', include('game.urls')),
                  path('v3/', include('payment.urls')),
                  path('v3/', include('order.urls')),
                  path('manager/', admin.site.urls),
                  path('', include('user.web_urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
