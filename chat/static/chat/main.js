const chatId = 1;
const socket = new WebSocket(`ws://<span class="math-inline">\{window\.location\.host\}/ws/chat/</span>{chatId}/`);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.message) {  // Check if message property exists
        const message = data.message;
        const messages = document.getElementById('messages');
        const messageElement = document.createElement('li');
        messageElement.textContent = `${message}: <span class="math-inline">\{message\.content\} \(</span>{message.timestamp})`;
        messages.appendChild(messageElement);
    } else {
        console.error('Received unexpected data from server');
    }
};

socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.getElementById('send-button').onclick = function() {
    const input = document.getElementById('message-input');
    const message = input.value;
    socket.send(JSON.stringify({
        'message': message
    }));
    input.value = '';
};
