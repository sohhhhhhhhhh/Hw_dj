document.addEventListener('DOMContentLoaded', () => {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Утилита для отправки запросов
  const sendRequest = async (url, method, data = null) => {
    const options = {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    };
    if (data) options.body = JSON.stringify(data);

    const response = await fetch(url, options);
    return response.json();
  };

  // Регистрация
  document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    const result = await sendRequest('/register/', 'POST', data);  // Убедитесь, что путь '/register/' совпадает с вашим маршрутом
    alert(result.message);
  });

  // Вход
  document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    const result = await sendRequest('/login/', 'POST', data);  // Убедитесь, что путь '/login/' совпадает с вашим маршрутом
    alert(result.message);
  });

  // Сброс пароля
  document.getElementById('password-reset-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    const result = await sendRequest('/password_reset/', 'POST', data);  // Путь для сброса пароля
    alert(result.message);
  });

  // Удаление аккаунта
  document.getElementById('delete-account-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const result = await sendRequest('/delete_account/', 'DELETE');  // Путь для удаления аккаунта
    alert(result.message);
  });

  // Обновление профиля
  document.getElementById('update-profile-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    const result = await sendRequest('/update_profile/', 'PUT', data);  // Путь для обновления профиля
    alert(result.message);
  });

  // Восстановление аккаунта через токен
  document.getElementById('restore-account-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    const result = await sendRequest('/restore_account/', 'POST', data);  // Путь для восстановления аккаунта
    alert(result.message);
  });
});
