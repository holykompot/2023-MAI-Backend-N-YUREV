from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('databases/', views.database_list, name='database_list'),
    path('databases/<int:database_id>/', views.database_detail, name='database_detail'),
    path('metrics/', views.metric_list, name='metric_list'),
]