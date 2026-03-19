// Простая регистрация — только имя, без проверок
(function() {
    // Получаем элементы
    const userNameInput = document.getElementById('userName');
    const registerBtn = document.getElementById('registerBtn');

    // Функция регистрации
    function register() {
        const userName = userNameInput.value.trim() || 'Гость';
        
        // Здесь будет ваш код для передачи имени в Python через Eel
        // Например: eel.register_user(userName)();
        
        // Пока просто показываем в консоли
        console.log('Зарегистрирован пользователь:', userName);
        
        // Здесь можно добавить редирект на главную страницу
        window.location.href = 'index.html';
    }

    // Обработчик на кнопку
    registerBtn.addEventListener('click', register);

    // Обработчик на Enter в поле ввода
    userNameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            register();
        }
    });

    // Автоматически фокусируемся на поле ввода
    userNameInput.focus();
})();