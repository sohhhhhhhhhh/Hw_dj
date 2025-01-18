from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt #Чтобы атаки не искал, токен мы не пишем энивей
from django.shortcuts import redirect
import json
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

def home(request):
    return JsonResponse({"message": "Первая лаба"})
def get_data(request):
    #Обрабатывает GET-запрос на /data и пишет сообщение
    return JsonResponse({
        "status": "success",
        "message": "Это API",
    })


def get_info(request):
    #Обрабатывает GET-запрос на /info и возвращает очень полезное сообщение
    return JsonResponse({
        "status": "success",
        "message": "Информация о нашем API",
        "data": {
            "plot": "эщкере",
        }
    })



def post_data(request):
    #Обрабатывает POST-запрос на /post_data
    #Добавила валидацию и персонализированные ответы
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Валидация
            if 'name' not in data or 'age' not in data:
                return JsonResponse({
                    "status": "error",
                    "message": "Ошибка: Укажи 'name' и 'age'."
                }, status=400)

            # Проверяем тип возраста
            if not isinstance(data['age'], int):
                return JsonResponse({
                    "status": "error",
                    "message": "Поле 'age' должно быть числом."
                }, status=400)

            # Норм ответ
            return JsonResponse({
                "status": "success",
                "message": f"Привет, {data['name']}! Тебе {data['age']} лет.",
                "hints": [
                    "Чекай /info"
                ]
            })

        except json.JSONDecodeError:
            # Если JSON некорректен
            return JsonResponse({
                "status": "error",
                "message": "Ошибка парсинга JSON: Проверь корректность данных."
            }, status=400)

    # Метод не поддерживается
    return JsonResponse({
        "status": "error",
        "message": "Метод не поддерживается. Используй POST."
    }, status=405)




def combined(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Это GET запрос на /combined"})
    elif request.method == 'POST':
        return redirect('/data/') #Редиректим если у нас пост запрос
    return JsonResponse({"error": "Метод не поддерживается"}, status=405)




def register(request):  # Регистрация
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message": "Пользователь уже существует"}, status=400)

            User.objects.create_user(username=username, password=password)
            return JsonResponse({"message": "Регистрация успешна"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Некорректные данные"}, status=400)

    # Ответ для других методов
    return JsonResponse({"message": "Метод не поддерживается"}, status=405)

#Вход в акк
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Вход выполнен"})
        return JsonResponse({"message": "Неверные учетные данные"}, status=401)


def user_list(request): #Смотрим и создаем пользователей (Create,read)
    if request.method == 'GET':
        users = list(CustomUser.objects.values())
        return JsonResponse(users, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        user = CustomUser.objects.create(**data)
        return JsonResponse({"id": user.id, "message": "Пользователь создан"}, status=201)
    return HttpResponseNotAllowed(['GET', 'POST'])


def user_detail(request, user_id): #Обнова и удаление (Update,delete)
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Пользователь не найден"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"id": user.id, "username": user.username})
    elif request.method == 'PUT':
        data = json.loads(request.body)
        for field, value in data.items():
            setattr(user, field, value)
        user.save()
        return JsonResponse({"message": "Пользователь обновлен"})
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({"message": "Пользователь удален"})
    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])



def password_reset(request): #Ресет пароля со стороны пользователя, делаем свой эндпоинт
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f""
            send_mail(
                'Пароль обновлен',
                f'Перейдите по ссылке чтобы обновить пароль: {reset_url}',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({"message": "Ссылка для сброса пароля у вас на почте"})
        except User.DoesNotExist:
            return JsonResponse({"message": "Не нашли вас"}, status=404)
    return HttpResponseNotAllowed(['POST'])

 #Удалялка со стороны пользователя
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return JsonResponse({"message": "Аккаунт усешно удален"})
    return HttpResponseNotAllowed(['DELETE'])


 #Апдейт со стороны пользователя
def update_profile(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        user = request.user
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()
        return JsonResponse({"message": "Заапдейтили вас"})
    return HttpResponseNotAllowed(['PUT'])

 #Восстановление через токен и SMTP
def restore_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        token = data.get('token')
        try:
            user = CustomUser.objects.get(email=email)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return JsonResponse({"message": "Восстановили вас"})
            else:
                return JsonResponse({"message": "Токен не тот, ищите новый"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "Пользователя нет вы че"}, status=404)
    return HttpResponseNotAllowed(['POST'])
