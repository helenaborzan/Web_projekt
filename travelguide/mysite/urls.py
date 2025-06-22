
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("travelApp/", include("travelApp.urls")),
    path('admin/', admin.site.urls),
]
