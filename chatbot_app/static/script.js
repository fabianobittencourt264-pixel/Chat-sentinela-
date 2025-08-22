document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');

    // Function to append a message to the chat window
    function appendMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        // Use innerText to prevent XSS attacks.
        messageElement.innerText = message;
        // Use 'pre-wrap' to respect newlines and wrap text.
        messageElement.style.whiteSpace = 'pre-wrap';

        chatWindow.appendChild(messageElement);
        // Scroll to the bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Function to show/hide typing indicator
    function setTyping(isTyping) {
        let indicator = document.querySelector('.typing-indicator');
        if (isTyping) {
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.classList.add('message', 'typing-indicator');
                indicator.innerText = 'Sentinela está digitando...';
                chatWindow.appendChild(indicator);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        } else {
            if (indicator) {
                indicator.remove();
            }
        }
    }

    // Greet the user when the chat loads
    appendMessage("Olá! Eu sou o Sentinela Nativense, seu assistente cívico. Como posso ajudar hoje?", 'bot');

    // Handle form submission
    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userMessage = messageInput.value.trim();

        if (userMessage === '') {
            return;
        }

        // Display user's message
        appendMessage(userMessage, 'user');
        messageInput.value = '';

        // Show typing indicator
        setTyping(true);

        try {
            // Send message to the backend
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            // Hide typing indicator
            setTyping(false);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Display bot's reply
            // The reply from the backend might have markdown-like formatting,
            // so we'll replace newlines with <br> for HTML rendering.
            // A more advanced version could parse markdown properly.
            const formattedReply = data.reply.replace(/\n/g, '\n'); // Keep newlines for pre-wrap
            appendMessage(formattedReply, 'bot');

        } catch (error) {
            console.error('Error fetching bot reply:', error);
            setTyping(false);
            appendMessage('Desculpe, ocorreu um erro de comunicação com o servidor. Tente novamente mais tarde.', 'bot');
        }
    });
});
