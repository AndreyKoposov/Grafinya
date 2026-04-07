function getConnectionChecker(fetch_request, timeout) {
    // Переменная для хранения интервала
    let intervalId = null;
    // Флаг для отслеживания состояния соединения
    let isConnected = false;
    
    // Функция для выполнения проверки соединения
    async function checkConnection() {
        try {
            const controller = new AbortController(); // Для прерывание запроса по истечению timeout
            const timeoutId = setTimeout(() => controller.abort(), timeout); // Запускаем таймер timeout
            const response = await fetch_request(controller.signal)
            clearTimeout(timeoutId); 
            const newStatus = response.ok;
            
            // Если статус изменился, вызываем соответствующий колбэк
            if (newStatus !== isConnected) {
                if (newStatus)
                    onConnectionRestored?.();
                else
                    onConnectionLost?.();
                isConnected = newStatus;
            }

            // Если нет - вызываем колбэк с результатом проверки
            onStatusChange?.(newStatus, response.status);
            
        } catch (error) {
            // Если произошла ошибка (сеть недоступна, таймаут и т.д.)
            if (error.name === 'AbortError') {
                console.log('Request timeout - connection may be slow or unavailable');
            }
            
            if (isConnected) {
                onConnectionLost?.();
                isConnected = false;
            }

            onStatusChange?.(false, null, error);
        }
    }
    
    // Колбэки для различных событий
    let onConnectionLost = null;
    let onConnectionRestored = null;
    let onStatusChange = null;
    
    // Запуск проверки
    function start() {
        if (intervalId === null) {
            // Сразу выполняем первую проверку
            checkConnection();
            // Затем запускаем интервал на секунду
            intervalId = setInterval(checkConnection, 1000);
            console.log('Connection checking started');
        }
    }
    
    // Остановка проверки
    function stop() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
            console.log('Connection checking stopped');
        }
    }
    
    // Методы для установки колбэков
    return {
        start,
        stop,
        onConnectionLost: (callback) => { onConnectionLost = callback; },
        onConnectionRestored: (callback) => { onConnectionRestored = callback; },
        onStatusChange: (callback) => { onStatusChange = callback; },
        isRunning: () => intervalId !== null,
        getCurrentStatus: () => isConnected
    };
}

function getMsgsChecker(fetch_request, timeout) {
    let intervalId = null;
    let hasNew = false;
    let aiThinking = false;
    
    async function checkMsgs() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            [hasNew, aiThinking] = await fetch_request(controller.signal)
            clearTimeout(timeoutId); 

            if (hasNew)
                onNew();

            if (!aiThinking)
                stop();
            
        } catch (error) {
            console.error(error)
        }
    }
    
    let onStop = null;
    
    function start() {
        if (intervalId === null) {
            checkMsgs();
            intervalId = setInterval(checkMsgs, 500);
            console.log('Msgs checking started');
        }
    }
    
    function stop() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
            console.log('Msgs checking stopped');
            onStop();
        }
    }

    return {
        start,
        stop,
        onNew: (callback) => { onNew = callback; },
        onStop: (callback) => { onStop = callback; },
    };
}