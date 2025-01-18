import requests #библиотека для работы с запросами, надо установить перед использованием
from django.http import JsonResponse
from django.http import HttpResponse

def forward_request(request):
    url = 'http://localhost:8001/api/endpoint'
    response = requests.get(url, params=request.GET)  # Прокси-запрос
    return JsonResponse(response.json())

def home(request):
    return HttpResponse("Страница есть")
