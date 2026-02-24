from django.urls import path
from Firstpage import views

app_name = 'firstpage'

urlpatterns = [
    path('', views.index, name='index'),
]
