from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf.urls.static import static
urlpatterns = [
    path('booking/', views.booking, name="booking_page"),
    path('choose-seat/<int:bookingId>/', views.select_seat, name="booking"),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)