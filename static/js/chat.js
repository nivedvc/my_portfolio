document.addEventListener('DOMContentLoaded', () => {
    const chatBubble = document.getElementById('chat-bubble');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const sendChat = document.getElementById('send-chat');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const suggestions = document.querySelectorAll('.suggestion');

    // Toggle Chat Window
    chatBubble.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            chatInput.focus();
        }
    });

    closeChat.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });

    // Handle Sending Messages
    async function sendMessage(message) {
        if (!message.trim()) return;

        // Add user message to UI
        appendMessage('user', message);
        chatInput.value = '';

        // Add loading indicator
        const loadingId = addLoadingIndicator();
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();

            // Remove loading and add AI response
            removeLoadingIndicator(loadingId);
            appendMessage('ai', data.response);
        } catch (error) {
            console.error('Error:', error);
            removeLoadingIndicator(loadingId);
            appendMessage('ai', "I'm sorry, I'm having trouble connecting right now. Please try again later.");
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = text;

        // Remove suggestions once a message is sent
        const existingSuggestions = chatMessages.querySelector('.suggested-questions');
        if (existingSuggestions) {
            existingSuggestions.remove();
        }

        chatMessages.appendChild(messageDiv);
    }

    function addLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message ai-message loading-indicator';
        loadingDiv.id = id;
        loadingDiv.innerHTML = `
            <div class="loading-dots">
                <span></span><span></span><span></span>
            </div>
        `;
        chatMessages.appendChild(loadingDiv);
        return id;
    }

    function removeLoadingIndicator(id) {
        const indicator = document.getElementById(id);
        if (indicator) indicator.remove();
    }

    // Event Listeners
    sendChat.addEventListener('click', () => {
        sendMessage(chatInput.value);
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(chatInput.value);
        }
    });

    suggestions.forEach(suggestion => {
        suggestion.addEventListener('click', () => {
            sendMessage(suggestion.textContent);
        });
    });
});
