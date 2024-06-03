const chatId = 1; // Пример идентификатора чата
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatId}/`);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('li');
    messageElement.textContent = message;
    messages.appendChild(messageElement);
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
