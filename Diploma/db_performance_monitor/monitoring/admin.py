from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Database, Metric, DatabaseMetric


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'db_type', 'host', 'port', 'owner')
    list_filter = ('db_type', 'owner')
    search_fields = ('name', 'host')


class MetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'unit')
    search_fields = ('name', 'description')


class DatabaseMetricAdmin(admin.ModelAdmin):
    list_display = ('database', 'metric', 'value', 'timestamp')
    list_filter = ('database', 'metric')
    search_fields = ('database__name', 'metric__name')

    # Внешний ключ "owner" связан с моделью "Database", поэтому используйте 'database__owner' для фильтрации.
    raw_id_fields = ('database', 'metric')  # Для упрощения выбора связанных объектов
    list_select_related = ('database', 'metric')


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(DatabaseMetric, DatabaseMetricAdmin)