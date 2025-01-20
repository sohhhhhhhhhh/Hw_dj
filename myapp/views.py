from django.http import HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.shortcuts import redirect, render
import json
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import logout

def home(request):
    # Если пользователь авторизован, перенаправляем на профиль
    if request.user.is_authenticated:
        return redirect('profile')  # Замените на имя вашего маршрута для профиля

    # Если пользователь не авторизован, перенаправляем на страницу регистрации
    return redirect('register')  # Замените на имя вашего маршрута для регистрации



def logout_user(request):
    logout(request)
    return redirect('home')


def profile(request):

    if request.session.get('register', False):
        # Убираем метку с сессии после первого редиректа
        del request.session['register']
        return render(request, 'forms.html', {'user_authenticated': True, 'message': 'Регистрация успешна!'})

    # Возвращаем страницу профиля, если никаких дополнительных действий не требуется
    return render(request, 'forms.html', {'user_authenticated': True})


def get_data(request):
    message = "Это API"
    return render(request, 'forms.html', {'message': message})


def get_info(request):
    message = "Информация о нашем API: эщкере"
    return render(request, 'forms.html', {'message': message})


def post_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'name' not in data or 'age' not in data:
                message = "Ошибка: Укажи 'name' и 'age'."
                return render(request, 'forms.html', {'message': message})

            if not isinstance(data['age'], int):
                message = "Поле 'age' должно быть числом."
                return render(request, 'forms.html', {'message': message})

            message = f"Привет, {data['name']}! Тебе {data['age']} лет."
            return render(request, 'forms.html', {'message': message})

        except json.JSONDecodeError:
            message = "Ошибка парсинга JSON: Проверь корректность данных."
            return render(request, 'forms.html', {'message': message})

    message = "Метод не поддерживается. Используй POST."
    return render(request, 'forms.html', {'message': message})


def combined(request):
    if request.method == 'GET':
        message = "Это GET запрос на /combined"
        return render(request, 'forms.html', {'message': message})
    elif request.method == 'POST':
        return redirect('/data/')
    message = "Метод не поддерживается"
    return render(request, 'forms.html', {'message': message})


def register(request):
    if request.method == 'POST':
        try:
            # Получаем данные из формы через request.POST
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Проверяем, существует ли пользователь с таким именем
            if CustomUser.objects.filter(username=username).exists():
                message = "Пользователь с таким именем уже существует."
                return render(request, 'forms.html', {'message': message})

            # Создаем нового пользователя
            CustomUser.objects.create_user(username=username, password=password, email=email)

            # Сохраняем в сессии, что пользователь только что зарегистрировался
            request.session['register'] = True

            return redirect('profile')

        except Exception as e:
            # Обрабатываем ошибку и выводим сообщение
            message = f"Произошла ошибка: {str(e)}"
            return render(request, 'forms.html', {'message': message})

    # Если метод запроса не POST, отображаем форму регистрации
    return render(request, 'forms.html', {'show_register_form': True})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')

            message = "Неверные учетные данные"
            return render(request, 'forms.html', {'message': message})

        except Exception as e:
            message = f"Произошла ошибка при входе: {str(e)}"
            return render(request, 'forms.html', {'message': message})

    return render(request, 'forms.html', {'show_login_form': True})


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f"http://127.0.0.1:8000/restore-account/{token}/{user.email}/"
            send_mail(
                'Сброс пароля',
                f'Перейдите по следующей ссылке, чтобы сбросить пароль: {reset_url}',
                '',
                [user.email],
                fail_silently=False,
            )
            message = "Инструкция по сбросу пароля отправлена на почту"
            return render(request, 'forms.html', {'message': message})

        except CustomUser.DoesNotExist:
            # Не раскрываем, существует ли пользователь с таким email
            message = "Инструкция по сбросу пароля отправлена на почту, если такой аккаунт существует"
            return render(request, 'forms.html', {'message': message})

        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            message = "Ошибка при отправке письма"
            return render(request, 'forms.html', {'message': message})

    return render(request, 'forms.html', {'show_password_reset_form': True})


def delete_account(request):
    # Проверяем, что пользователь аутентифицирован
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                # Удаляем пользователя
                user = request.user
                user.delete()
                return redirect('register')  # Перенаправление на страницу регистрации после удаления

            except Exception as e:
                # Обрабатываем ошибку, если она возникла
                message = f"Произошла ошибка: {str(e)}"
                return render(request, 'forms.html', {'message': message})

        # Отображаем форму удаления аккаунта (если запрос GET)
        return render(request, 'forms.html', {'show_delete_account_form': True})

    # Если пользователь не авторизован, перенаправляем на страницу регистрации
    return redirect('register')


def update_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = request.user
            if username:
                user.username = username
            if password:
                user.set_password(password)
            if email:
                user.email = email
            user.save()
            return redirect('profile')

        message = "Необходимо авторизоваться"
        return render(request, 'forms.html', {'message': message})

    return render(request, 'forms.html', {'show_update_profile_form': True})



def restore_account(request, token, email):
    try:
        user = CustomUser.objects.get(email=email)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
                else:
                    message = "Некорректный пароль"
                    return render(request, 'forms.html', {'message': message})

            form = SetPasswordForm(user)
            return render(request, 'forms.html', {'form': form, 'show_restore_account_form': True})

        else:
            message = "Неверный или истекший токен"
            return render(request, 'forms.html', {'message': message})

    except CustomUser.DoesNotExist:
        message = "Пользователь с таким email не найден"
        return render(request, 'forms.html', {'message': message})
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        return render(request, 'forms.html', {'message': message})
