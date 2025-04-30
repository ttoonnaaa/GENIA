document.addEventListener('DOMContentLoaded', () => {
    const chatIcon = document.getElementById('chatIcon');
    const chatWindow = document.getElementById('chatWindow');
    const closeChat = document.getElementById('closeChat');
    const sendMessage = document.getElementById('sendMessage');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');

    // Toggle chat window
    chatIcon?.addEventListener('click', () => {
        chatWindow?.classList.toggle('active');
    });

    // Close chat window
    closeChat?.addEventListener('click', () => {
        chatWindow?.classList.remove('active');
    });

    // Send user message
    sendMessage?.addEventListener('click', sendUserMessage);
    userInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendUserMessage();
    });

    function sendUserMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        userInput.value = '';

        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: message }),
        })
        .then(async (response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('⚠️ Bot response missing.', 'bot');
            }
        })
        .catch((error) => {
            console.error('Fetch error:', error);
            addMessage('⚠️ Something went wrong. Try again later.', 'bot');
        });
    }

    // Send voice message
    const sendVoiceButton = document.getElementById('sendVoice');
    sendVoiceButton?.addEventListener('click', () => {
        const fileInput = document.getElementById('audioInput');
        if (!fileInput.files.length) return alert('يرجى اختيار ملف صوتي');

        const formData = new FormData();
        formData.append('audio', fileInput.files[0]);

        fetch('http://127.0.0.1:5000/voice', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('⚠️ لم يتم التعرف على الصوت.', 'bot');
            }
        })
        .catch(err => {
            console.error(err);
            addMessage('⚠️ حدث خطأ أثناء إرسال الصوت.', 'bot');
        });
    });

    // Add message to the chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerText = text;
        messageDiv.setAttribute('dir', 'rtl'); // Ensure Arabic text alignment
        messageDiv.style.textAlign = 'right';

        chatMessages?.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
