from django.urls import path
from . import views

app_name = "payFine"

urlpatterns = [
    path('', views.index, name='index'),
    path('refreshFines/', views.refreshFines, name='refreshFines'),
    path('makePayment/', views.makePayment, name='makePayment'),
]
