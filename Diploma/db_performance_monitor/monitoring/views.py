
# Create your views here.
from django.shortcuts import render
from .models import Database, DatabaseMetric


def database_list(request):
    databases = Database.objects.all()
    return render(request, 'monitoring/database_list.html', {'databases': databases})


def database_detail(request, database_id):
    database = Database.objects.get(pk=database_id)
    metrics = DatabaseMetric.objects.filter(database=database)
    return render(request, 'monitoring/database_detail.html', {'database': database, 'metrics': metrics})


def metric_list(request):
    metrics = DatabaseMetric.objects.all()
    return render(request, 'monitoring/metric_list.html', {'metrics': metrics})
