// Add this to your static/js/chat.js file
function initializeChat() {
    const messageContainer = document.querySelector('.threads');
    const messageForm = document.querySelector('.room__message form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let lastMessageTimestamp = messageContainer.lastElementChild ? 
        messageContainer.lastElementChild.dataset.timestamp : '1970-01-01T00:00:00Z';

    // Handle message submission
    messageForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const messageInput = messageForm.querySelector('input[name="body"]');
        const message = messageInput.value;
        
        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({
                    'body': message
                })
            });
            
            if (response.ok) {
                messageInput.value = '';
                const data = await response.json();
                appendMessage(data.message);
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    });

    // Function to append a new message to the chat
    function appendMessage(message) {
        const messageHTML = `
            <div class="thread" data-timestamp="${message.created}">
                <div class="thread__top">
                    <div class="thread__author">
                        <a href="/profile/${message.user_id}" class="thread__authorInfo">
                            <div class="avatar avatar--small">
                                <img src="${message.avatar_url}" />
                            </div>
                            <span>@${message.user}</span>
                        </a>
                        <span class="thread__date">just now</span>
                    </div>
                    ${message.can_delete ? `
                        <a href="/delete-message/${message.id}">
                            <div class="thread__delete">
                                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                                    <title>remove</title>
                                    <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
                                </svg>
                            </div>
                        </a>
                    ` : ''}
                </div>
                <div class="thread__details">
                    ${message.body}
                </div>
            </div>
        `;
        messageContainer.insertAdjacentHTML('beforeend', messageHTML);
        messageContainer.scrollTop = messageContainer.scrollHeight;
        lastMessageTimestamp = message.created;
    }

    // Poll for new messages
    async function pollNewMessages() {
        try {
            const response = await fetch(`${window.location.pathname}/messages?since=${lastMessageTimestamp}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                data.messages.forEach(message => {
                    appendMessage(message);
                });
            }
        } catch (error) {
            console.error('Error polling messages:', error);
        }
    }

    // Start polling every 2 seconds
    setInterval(pollNewMessages, 2000);
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeChat);