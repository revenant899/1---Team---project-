from django.urls import path
from Firstpage import views

urlpatterns = [
    path('', views.index, name='index'),
]
