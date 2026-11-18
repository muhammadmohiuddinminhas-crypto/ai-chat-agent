
async function sendMessage() {

    const input = document.getElementById("message");
    const button = document.getElementById("send-button");
    const message = input.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    button.disabled = true;
    input.disabled = true;

    const userMessage = document.createElement("div");
    userMessage.className = "user-msg";
    userMessage.textContent = "You: " + message;
    chatBox.appendChild(userMessage);

    input.value = "";

    const loadingMessage = document.createElement("div");
    loadingMessage.className = "bot-msg loading";
    loadingMessage.textContent = "AI is thinking...";
    chatBox.appendChild(loadingMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/send", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        loadingMessage.remove();

        // DAILY LIMIT REACHED

        if (data.limit_reached) {

            const limitMessage = document.createElement("div");
            limitMessage.className = "bot-msg error";
            limitMessage.textContent =
                "You have reached your daily limit of 100 messages.";

            chatBox.appendChild(limitMessage);

            const premiumLink = document.createElement("a");
            premiumLink.href = "/premium";
            premiumLink.textContent = "Explore Premium";
            premiumLink.className = "premium-link";

            chatBox.appendChild(premiumLink);

            button.disabled = true;
            input.disabled = true;

            chatBox.scrollTop = chatBox.scrollHeight;

            return;
        }

        // API ERROR

        if (!response.ok) {
            throw new Error(
                data.error || "Something went wrong"
            );
        }

        // SHOW AI RESPONSE

        const botMessage = document.createElement("div");
        botMessage.className = "bot-msg";
        botMessage.textContent = "AI: " + data.reply;
        chatBox.appendChild(botMessage);

        // UPDATE MESSAGE COUNTER

        if (data.message_count !== undefined) {

            document.getElementById("message-count").textContent =
                data.message_count;

        }

        if (data.remaining_messages !== undefined) {

            document.getElementById("remaining-messages").textContent =
                data.remaining_messages + " remaining";

        }

        chatBox.scrollTop = chatBox.scrollHeight;

    }

    catch (error) {

        loadingMessage.remove();

        const errorMessage = document.createElement("div");
        errorMessage.className = "bot-msg error";
        errorMessage.textContent = "Error: " + error.message;

        chatBox.appendChild(errorMessage);

        chatBox.scrollTop = chatBox.scrollHeight;

    }

    finally {

        // Keep input disabled if the daily limit is reached

        const remaining = document.getElementById("remaining-messages");

        if (!remaining || !remaining.textContent.startsWith("0 ")) {
            button.disabled = false;
            input.disabled = false;
            input.focus();
        }

    }

}


// ENTER KEY SUPPORT

document
    .getElementById("message")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }

    });
