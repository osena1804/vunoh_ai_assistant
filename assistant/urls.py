from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/process/', views.process_message, name='process_message'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/update-status/<str:task_code>/', views.update_status, name='update_status'),
]