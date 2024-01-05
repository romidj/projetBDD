from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path


urlpatterns = [
    path('adminn/', views.admin_dashboard, name='admin_dashboard'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('remove_movie/<int:movie_id>/', views.remove_movie, name='remove_movie'),
    path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)