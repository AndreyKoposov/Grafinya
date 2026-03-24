window.onload = function() {
    checkSession();
}

async function checkSession() {
    if (await auth())
        showSuccess();
    else
        showError();
}

async function auth() {
    var success = false;

    await fetch("http://127.0.0.1:8000/api/auth/login", {
        method: "POST"
    }).then(response => response.json())
        .then(data => success = data.success)
        .catch(error => console.error(error));

    return success
}

function showSuccess() {
    const iconContainer = document.getElementById('iconContainer');
    const loadingText = document.getElementById('loadingText');
    
    iconContainer.innerHTML = '<div class="checkmark"></div>';
    loadingText.textContent = 'Успешная аутентификация!';
    loadingText.classList.add('success');
    
    setTimeout(() => {
        window.location.href = '';
    }, 2000);
}

function showError() {
    const iconContainer = document.getElementById('iconContainer');
    const loadingText = document.getElementById('loadingText');
    const retryButton = document.getElementById('retryButton');
    
    iconContainer.innerHTML = '<div class="cross"></div>';
    loadingText.textContent = 'Ошибка аутентификации';
    loadingText.classList.add('error');

    retryButton.style.display = 'block';
}