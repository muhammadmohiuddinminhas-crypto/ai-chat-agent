async function sendMessage() {

    const input = document.getElementById("message")
    const message = input.value

    if (!message) {
        return
    }

    const chatBox = document.getElementById("chat-box")

    chatBox.innerHTML += `
        <div class="user-msg">
            <b>You:<