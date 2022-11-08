from django.urls import path
from . import views

app_name = "bookCheckIn"

urlpatterns = [
    path('', views.index, name='index'),
    path('checkin/', views.checkin, name='checkin')
]
