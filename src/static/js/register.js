// Простая регистрация — только имя, без проверок
(function() {
    // Получаем элементы
    const registerBtn = document.getElementById('registerBtn');

    // Функция регистрации
    async function register() {
        // Здесь будет ваш код для передачи имени в Python через Eel
        await fetch("http://127.0.0.1:8000/api/auth/login", {
            method: "POST"
        }).then(response => response.json())  
            .then(data => alert(data.success))
            .catch(error => console.error(error));
        
        // Здесь можно добавить редирект на главную страницу
        //window.location.href = 'index.html';
    }

    // Обработчик на кнопку
    registerBtn.addEventListener('click', register);
})();