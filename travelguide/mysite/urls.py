
from django.contrib import admin
from django.urls import include, path
from travelApp.views import home
from django.contrib.auth import views as auth_views
from travelApp.views import custom_logout



urlpatterns = [
    path("travelApp/", include("travelApp.urls")),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("travelApp/", include("django.contrib.auth.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),

]
