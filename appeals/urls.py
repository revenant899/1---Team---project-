from django.urls import path
from . import views

app_name = 'appeals'

urlpatterns = [
    path('adminpanel/', views.admin_panel, name='appeals_adminpanel'),
    path('create/', views.appeal_create, name='appeal_create'),
    path('update/<int:pk>/', views.appeal_update, name='appeal_update'),
    path('delete/<int:pk>/', views.appeal_delete, name='appeal_delete'),
    path('status/<int:pk>/', views.appeal_status, name='appeal_status'),
    path("detail/<int:pk>/", views.appeal_detail, name="appeal_detail"),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
    path("logs/", views.admin_logs, name="admin_logs"),
]