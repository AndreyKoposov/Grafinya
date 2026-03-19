// Простая регистрация — только имя, без проверок
(function() {
    // Получаем элементы
    const userNameInput = document.getElementById('userName');
    const registerBtn = document.getElementById('registerBtn');

    // Функция регистрации
    async function register() {
        const userName = userNameInput.value.trim() || 'Гость';
        
        // Здесь будет ваш код для передачи имени в Python через Eel
        const response = await fetch("http://127.0.0.1:8000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name: userName, orioks_id: "8213532" }),
        });
        alert(response)

        // Пока просто показываем в консоли
        console.log('Зарегистрирован пользователь:', userName);
        
        // Здесь можно добавить редирект на главную страницу
        //window.location.href = 'index.html';
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