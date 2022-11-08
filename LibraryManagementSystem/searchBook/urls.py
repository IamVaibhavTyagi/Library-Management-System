from django.urls import path
from . import views

app_name = "searchBook"

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout')

]
