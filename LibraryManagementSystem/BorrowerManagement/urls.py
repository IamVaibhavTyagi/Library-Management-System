from django.urls import path
from . import views

app_name = "BorrowerManagement"

urlpatterns = [
    path('', views.index, name='index'),

]
