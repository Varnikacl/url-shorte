var socket = io();

socket.on('message', function(msg) {
    var messages = document.getElementById('messages');
    var messageItem = document.createElement('div');
    messageItem.textContent = msg;
    messages.appendChild(messageItem);
});

function sendMessage() {
    var input = document.getElementById("message");
    var message = input.value;
    socket.send(message);
    input.value = '';
}