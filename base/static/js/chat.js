const initChat = (roomId) => {
    let chatSocket;

    // Function to create WebSocket connection
    function connectWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/base/room/${roomId}/`;
        
        chatSocket = new WebSocket(wsUrl);

        chatSocket.onopen = function(e) {
            console.log('WebSocket connection established');
        };

        chatSocket.onerror = function(e) {
            console.error('WebSocket error:', e);
            setTimeout(connectWebSocket, 5000);
        };

        chatSocket.onclose = function(e) {
            console.log('WebSocket connection closed');
            setTimeout(connectWebSocket, 5000);
        };

        chatSocket.onmessage = function(e) {
            try {
                const data = JSON.parse(e.data);
                const messageElement = document.createElement('div');
                messageElement.classList.add('thread');
                messageElement.innerHTML = `
                    <div class="thread__top">
                        <div class="thread__author">
                            <div class="avatar avatar--small">
                                <img src="${data.user_avatar}" alt="User avatar" />
                            </div>
                            <span>@${data.username}</span>
                            <span class="thread__date">${data.timestamp}</span>
                        </div>
                    </div>
                    <div class="thread__details">${data.message}</div>
                `;
                const chatLog = document.querySelector('#chat-log');
                chatLog.insertBefore(messageElement, chatLog.firstChild);
                chatLog.scrollTop = 0;

                // Check if the message is a video call notification
                if (data.type === 'video-call-started') {
                    document.getElementById('videoCallNotification').style.display = 'block';
                }
            } catch (error) {
                console.error('Error processing message:', error);
            }
        };
    }

    // Initial connection
    connectWebSocket();

    // Handle form submission and Enter key press
    const messageInput = document.querySelector('#chat-message-input');
    const sendMessage = () => {
        const message = messageInput.value.trim();
        if (message && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
            const chatLog = document.querySelector('#chat-log');
            chatLog.scrollTop = 0;
        }
    };

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    // Handle form submit button
    const form = messageInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            sendMessage();
        });
    }

    // Set up chat scroll behavior
    document.addEventListener('DOMContentLoaded', function() {
        const chatLog = document.querySelector('#chat-log');
        chatLog.style.display = 'flex';
        chatLog.style.flexDirection = 'column-reverse';
        chatLog.scrollTop = 0;
    });

    return chatSocket;
};

export default initChat;