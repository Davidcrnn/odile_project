from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('main.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('admin/', admin.site.urls),
        path('accounts/', include('allauth.urls')),
        path('', include('main.urls')),
    ]


handler404 = 'main.views.custom_error_404_view'
handler404 = 'main.views.custom_error_500_view'
# handler500 = 'main.views.custom_error_view'
