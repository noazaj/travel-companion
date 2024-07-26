document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const chatBox = document.getElementById("chat-box");

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const userInput = document.getElementById("user-input").value;

        if (userInput.trim() !== "") {
            appendMessage(userInput, "user");
            document.getElementById("user-input").value = "";

            // Send user input to the server and get the response
            fetch(chatForm.action, {
                method: "POST",
                body: new URLSearchParams(new FormData(chatForm)),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.response) {
                        appendMessage(data.response, "bot");
                    }
                })
                .catch(error => console.error("Error:", error));
        }
    });

    function appendMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", sender);

        const messageContent = document.createElement("div");
        messageContent.classList.add("message");
        messageContent.textContent = message;

        messageElement.appendChild(messageContent);
        chatBox.appendChild(messageElement);

        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
