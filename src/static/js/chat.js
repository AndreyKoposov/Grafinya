function startChat() {
    // Состояние чата
    const chatState = {
        messages: [],
        isTyping: false,
        userId: 'user',
        assistantId: 'ai'
    };

    // DOM элементы
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMessageBtn');
    const commandButtons = document.getElementById('commandButtons');

    // Инициализация чата
    function initChat() {
        if (!chatMessages || !chatInput || !sendBtn) {
            console.warn('Элементы чата не найдены');
            return;
        }

        // Загружаем сохраненные сообщения (если есть)
        loadMessages();
        
        // Добавляем обработчики событий
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', handleKeyPress);
        
        // Обработчики для командных кнопок
        if (commandButtons) {
            commandButtons.querySelectorAll('.command-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    chatInput.value = btn.dataset.command + ' ';
                    chatInput.focus();
                });
            });
        }

        // Скроллим вниз
        scrollToBottom();
    }
    // Загрузка сообщений
    async function loadMessages() {
        chatState.messages = []
        var story = await api_fetch_msgs()
        for (var i = 0; i < story.length; i++) {
            msg = story[i]
            chatState.messages.push({
                text: msg["text"],
                sender: msg["sender"],
                time: msg["time"],
                id: i
            });
        }
        renderMessages();
    }
    // Отправка сообщения
    async function sendMessage() {
        // Отправляем сообщение пользователя
        const text = chatInput.value.trim();
        if (!text) return;
        chatInput.value = '';
        await api_send_msg(text)
        await loadMessages()

        showTypingIndicator();
        await loadMessages()
        hideTypingIndicator();
    }

    // Отрисовка всех сообщений
    function renderMessages() {
        if (!chatMessages) return;
        
        chatMessages.innerHTML = '';
        chatState.messages.forEach(msg => renderMessage(msg));
        scrollToBottom();
    }
    // Отрисовка одного сообщения
    function renderMessage(message) {
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.sender}`;
        messageDiv.dataset.id = message.id;
        
        messageDiv.innerHTML = `
            <div class="message-bubble">
                ${message.text.replace(/\n/g, '<br>')}
                <div class="message-time">${message.time}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
    }
    // Показать индикатор печатания
    function showTypingIndicator() {
        if (chatState.isTyping) return;
        
        chatState.isTyping = true;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }
    // Скрыть индикатор печатания
    function hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
        chatState.isTyping = false;
    }
    // Скролл вниз
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    // Обработка нажатия Enter
    function handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    initChat();
}