from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('favorites/', include('favorites.urls')),
    path('about/', include('about.urls')),
]

handler404 = 'about.views.page_404'
handler500 = 'about.views.page_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
