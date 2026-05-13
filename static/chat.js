async function sendMessage() {

    const input = document.getElementById("message")
    const message = input.value.trim()

    if (!message) return

    const chatBox = document.getElementById("chat-box")

    // show user message
    chatBox.innerHTML += `
        <div class="user-msg">
            <b>You:</b> ${message}
        </div>
    `

    input.value = ""

    // send to backend
    const response = await fetch("/send", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })

    const data = await response.json()

    // show AI response
    chatBox.innerHTML += `
        <div class="bot-msg">
            <b>AI:</b> ${data.reply}
        </div>
    `

    chatBox.scrollTop = chatBox.scrollHeight
}