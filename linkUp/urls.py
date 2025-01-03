
from django.contrib import admin # type: ignore 
from django.urls import path, include # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
# from base.urls

# super user :
# username = sahil
# password = S#@5ahil1P
# email = sahilvanarse13@gmail.com


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
