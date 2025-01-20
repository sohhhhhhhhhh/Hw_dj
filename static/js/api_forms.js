document.addEventListener('DOMContentLoaded', () => {
  // Получаем csrf токен
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Универсальная функция для отправки запроса
  async function sendRequest(url, method, data) {
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // Добавляем CSRF токен в заголовки
      },
      body: JSON.stringify(data),  // Отправляем данные как JSON
    });

    if (!response.ok) {
      throw new Error(`HTTP error! статус: ${response.status}`);
    }

    // Логируем ответ перед обработкой
    const textResponse = await response.text();
    console.log('Ответ от сервера:', textResponse);

    // Проверка, что ответ содержит JSON
    const contentType = response.headers.get('Content-Type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Ответ не в формате JSON');
    }

    // Попробуем парсить только если это JSON
    try {
      const result = JSON.parse(textResponse);
      showPopup(result.message);
    } catch (error) {
      console.error('Ошибка при парсинге JSON:', error);
      showPopup('Ошибка при получении данных от сервера');
    }
  }

  // Функция для отображения попапа
  function showPopup(message) {
    const popup = document.createElement('div');
    popup.classList.add('popup');
    popup.innerHTML = `
      <div class="popup-content">
        <p>${message}</p>
        <button class="close-btn">Закрыть</button>
      </div>
    `;
    document.body.appendChild(popup);

    // Закрытие попапа
    document.querySelector('.close-btn').addEventListener('click', () => {
      document.body.removeChild(popup);
    });
  }

  // Универсальная функция для обработки отправки формы
  function handleFormSubmit(formId, method, url) {
    const form = document.getElementById(formId);
    if (form) {
      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());  // Преобразуем FormData в обычный объект
        await sendRequest(url, method, data);  // Отправляем запрос
      });
    }
  }

  // Использование универсальной функции для всех формочек
  handleFormSubmit('register-form', 'POST', '/register/');
  handleFormSubmit('login-form', 'POST', '/login/');
  handleFormSubmit('password-reset-form', 'POST', '/password_reset/');
  handleFormSubmit('delete-account-form', 'DELETE', '/delete_account/');
  handleFormSubmit('update-profile-form', 'PUT', '/update_profile/');
  handleFormSubmit('restore-account-form', 'POST', '/restore_account/');
});
