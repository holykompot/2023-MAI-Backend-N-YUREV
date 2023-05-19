from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('products/', views.products, name='products'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('get_all_films/', views.get_all_films, name='get_all_films'),
    path('create_film/', views.create_film, name='create_film'),

]