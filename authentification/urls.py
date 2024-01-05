from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.landing, name="landing"),
    path('signin', views.signin, name="signin"),
    path('login', views.login, name="login"),
    path('signout', views.logout, name="signout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)