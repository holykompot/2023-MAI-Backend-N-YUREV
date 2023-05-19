from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from .models import Producer, Films


def profile(request):
    if request.method == 'GET':
        return JsonResponse({"data": "User profile"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def products(request):
    if request.method == 'GET':
        return JsonResponse({"data": "List of products"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def category(request, category_id):
    if request.method == 'GET':
        return JsonResponse({"data": f"Category {category_id}"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def search(request):
    query = request.GET.get('q', '')

    if query:
        results = Films.objects.filter(Q(titleicontains=query) | Q(authorname__icontains=query))
    else:
        results = []

    response_data = [{'id': film.id, 'title': film.title, 'author': film.producer.name} for film in results]
    return JsonResponse({'data': response_data})


def get_all_films(request):
    if request.method == 'GET':
        films = Films.objects.all()
        response_data = [{'id': film.id, 'title': film.title, 'author': film.producer.name} for film in films]
        return JsonResponse({'data': response_data})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def create_film(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        producername = request.POST.get('producer')

        author, = Producer.objects.get_or_create(name=producername)
        film = Films.objects.create(title=title, author=author)
        film.save()

        return JsonResponse({'message': 'Film created successfully', 'id': film.id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
