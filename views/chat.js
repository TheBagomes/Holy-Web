let socket = new WebSocket(`ws://${window.location.host}/ws`);

// Quando receber mensagem
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    addMessageToChat(data.username, data.message, data.isMine);
};

// ELEMENTOS DOM
const input = document.getElementById("chat-input");
const btn = document.getElementById("btn-chat");
const chatBox = document.getElementById("chat-box");

// ENVIAR MENSAGEM
function sendMessage() {
    const text = input.value.trim();
    if (text === "") return;

    const payload = {
        message: text,
        time: new Date().toLocaleTimeString()
    };

    socket.send(JSON.stringify(payload));
    input.value = "";
}

btn.onclick = sendMessage;

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

// ADICIONAR MENSAGEM NO CHAT
function addMessageToChat(username, text, isMine) {
    const div = document.createElement("div");

    div.innerHTML = `
        <div class="bubble ${isMine ? "mine" : "theirs"}">
            <strong>${username}:</strong> ${text}
        </div>
    `;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
