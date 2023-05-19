from django.contrib import admin
from .models import Producer, Category, Films, UserProfile


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


admin.site.register(Producer, ProducerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)


class FilmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'producer',)
    search_fields = ('title',)
    list_filter = ('producer',)


admin.site.register(Films, FilmsAdmin)


