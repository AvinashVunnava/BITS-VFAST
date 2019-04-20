from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check_availability$', views.check_availability, name='check_availability'),
    url(r'^student_booking$', views.student_booking, name='student_booking'),
    url(r'get_bookings', views.get_bookings, name='get_bookings')
]
