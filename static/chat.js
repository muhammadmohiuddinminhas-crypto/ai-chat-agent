
// ==========================================
// CHAT SESSION MANAGEMENT
// ==========================================

let currentChatSessionId = null;


// ==========================================
// LOAD CHAT HISTORY SIDEBAR
// ==========================================

async function loadChatHistoryList() {

    const historyList = document.getElementById(
        "chat-history-list"
    );

    try {

        const response = await fetch("/chat_history");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to load history.");
        }

        historyList.innerHTML = "";

        if (!data.history || data.history.length === 0) {

            historyList.innerHTML =
                '<p class="history-empty">No conversations yet.</p>';

            return;
        }

        data.history.forEach(session => {

            const item = document.createElement("button");

            item.className = "history-item";

            item.textContent = session.title;

            item.dataset.sessionId = session.id;

            if (Number(session.id) === Number(currentChatSessionId)) {
                item.classList.add("active");
            }

            item.addEventListener("click", function() {
                loadChatSession(session.id);
            });

            historyList.appendChild(item);

        });

        filterChatHistory();

    }

    catch (error) {

        historyList.innerHTML =
            '<p class="history-empty">Unable to load conversations.</p>';

        console.error("Chat history error:", error);

    }

}


// ==========================================
// OPEN EXISTING CHAT SESSION
// ==========================================

async function loadChatSession(sessionId) {

    const chatBox = document.getElementById("chat-box");

    const titleElement = document.getElementById(
        "current-chat-title"
    );

    try {

        const response = await fetch(
            `/chat_history/${encodeURIComponent(sessionId)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to open conversation.");
        }

        currentChatSessionId = data.session_id;

        titleElement.textContent = data.title;

        chatBox.innerHTML = "";

        data.messages.forEach(message => {

            const userMessage = document.createElement("div");

            userMessage.className = "user-msg";

            userMessage.textContent =
                "You: " + message.user_message;

            chatBox.appendChild(userMessage);


            const botMessage = document.createElement("div");

            botMessage.className = "bot-msg";

            botMessage.textContent =
                "AI: " + message.bot_response;

            chatBox.appendChild(botMessage);

        });

        chatBox.scrollTop = chatBox.scrollHeight;

        await loadChatHistoryList();

    }

    catch (error) {

        alert(error.message);

        console.error("Unable to open chat:", error);

    }

}


// ==========================================
// START NEW CHAT
// ==========================================

function startNewChat() {

    currentChatSessionId = null;

    const chatBox = document.getElementById("chat-box");

    const titleElement = document.getElementById(
        "current-chat-title"
    );

    const input = document.getElementById("message");

    const button = document.getElementById("send-button");

    chatBox.innerHTML = `
        <div class="welcome-message">
            <h3>New Conversation ðŸ‘‹</h3>
            <p>How can I help you today?</p>
        </div>
    `;

    titleElement.textContent = "AI Agent 1.0";

    document.querySelectorAll(".history-item").forEach(item => {
        item.classList.remove("active");
    });

    const remaining = document.getElementById("remaining-messages");

    if (!remaining.textContent.startsWith("0 ")) {

        input.disabled = false;
        button.disabled = false;

    }

    input.focus();

}


// ==========================================
// SEARCH CHAT HISTORY
// ==========================================

function filterChatHistory() {

    const searchInput = document.getElementById(
        "history-search"
    );

    const searchText = searchInput.value.toLowerCase();

    document.querySelectorAll(".history-item").forEach(item => {

        const title = item.textContent.toLowerCase();

        item.style.display = title.includes(searchText)
            ? "block"
            : "none";

    });

}


// ==========================================
// SEND MESSAGE
// ==========================================

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

                message: message,

                chat_session_id: currentChatSessionId

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

            chatBox.scrollTop = chatBox.scrollHeight;

            button.disabled = true;

            input.disabled = true;

            return;

        }


        // API ERROR

        if (!response.ok) {

            throw new Error(
                data.error || "Something went wrong."
            );

        }


        // SAVE ACTIVE SESSION ID

        currentChatSessionId = data.chat_session_id;

        document.getElementById(
            "current-chat-title"
        ).textContent = data.chat_title;


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


        // REFRESH SIDEBAR

        await loadChatHistoryList();

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

        const remaining = document.getElementById(
            "remaining-messages"
        );

        if (!remaining || !remaining.textContent.startsWith("0 ")) {

            button.disabled = false;

            input.disabled = false;

            input.focus();

        }

    }

}


// ==========================================
// ENTER KEY SUPPORT
// ==========================================

document.getElementById("message").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


// ==========================================
// SEARCH INPUT EVENT
// ==========================================

document.getElementById("history-search").addEventListener(
    "input",
    filterChatHistory
);



// ==========================================
// MOBILE SIDEBAR MENU
// ==========================================

const appLayout = document.querySelector(".app-layout");

const menuButton = document.getElementById(
    "mobile-menu-button"
);

const sidebarOverlay = document.getElementById(
    "sidebar-overlay"
);


function openSidebar() {

    appLayout.classList.add("sidebar-open");

    menuButton.setAttribute("aria-expanded", "true");

}


function closeSidebar() {

    appLayout.classList.remove("sidebar-open");

    menuButton.setAttribute("aria-expanded", "false");

}


if (menuButton && sidebarOverlay && appLayout) {

    menuButton.addEventListener("click", function() {

        if (appLayout.classList.contains("sidebar-open")) {

            closeSidebar();

        } else {

            openSidebar();

        }

    });


    sidebarOverlay.addEventListener("click", closeSidebar);


    document.addEventListener("keydown", function(event) {

        if (event.key === "Escape") {

            closeSidebar();

        }

    });


    // Close sidebar when selecting a conversation

    document.getElementById("chat-history-list")
        .addEventListener("click", function(event) {

            if (event.target.closest(".history-item")) {

                closeSidebar();

            }

        });


    // Close sidebar when selecting Settings or Logout

    document.querySelectorAll(".sidebar-footer a")
        .forEach(link => {

            link.addEventListener("click", closeSidebar);

        });


    // Close sidebar after starting a new chat

    document.getElementById("new-chat-button")
        .addEventListener("click", closeSidebar);

}


// ==========================================
// INITIALIZE CHAT DASHBOARD
// ==========================================

loadChatHistoryList();

