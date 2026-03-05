from django.urls import path
from Firstpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assign/<int:pk>/', views.assign_ticket, name='assign_ticket'),
]