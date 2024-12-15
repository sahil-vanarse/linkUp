
from django.contrib import admin
from django.urls import path, include
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
