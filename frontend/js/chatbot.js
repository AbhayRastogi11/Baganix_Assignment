document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const typingIndicator = document.getElementById("typing-indicator");

    // WebSocket connection
    const socket = new WebSocket("ws://localhost:8000/ws/testuser");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });

    socket.onmessage = function (event) {
        hideTypingIndicator();
        let botMessage = event.data;

        try {
            let parsedData = JSON.parse(botMessage);
            if (parsedData.response) {
                botMessage = parsedData.response;
            }
        } catch (e) { }

        addMessage(botMessage, "bot");
    };

    function sendMessage() {
        let message = userInput.value.trim();
        if (message === "") return;

        addMessage(message, "user");
        userInput.value = "";
        showTypingIndicator();

        socket.send(message);
    }

    function addMessage(text, sender) {
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        typingIndicator.style.visibility = "visible";
    }

    function hideTypingIndicator() {
        typingIndicator.style.visibility = "hidden";
    }
});
