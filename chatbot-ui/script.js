
// Generate unique session ID when page loads
window.addEventListener("DOMContentLoaded", () => {
    const sessionIdField = document.getElementById("session-id");
    const uniqueId = crypto.randomUUID(); // Use a better random unique ID
    sessionIdField.value = uniqueId;
    sessionIdField.readOnly = true; // Make it read-only so users can't change
});
let lockedSessionId = localStorage.getItem("lockedSessionId");

if (!lockedSessionId) {
    lockedSessionId = "session_" + Date.now() + "_" + Math.floor(Math.random() * 10000);
    localStorage.setItem("lockedSessionId", lockedSessionId);
}

// Set it to the input (readonly)
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("session-id").value = lockedSessionId;
});

  
async function sendMessage(event) {
    if (event) event.preventDefault();

    const sessionId = document.getElementById("session-id").value.trim();
    const userInput = document.getElementById("user-input").value.trim();
    const chatBox = document.getElementById("chat-box");

    if (!sessionId || !userInput) {
        alert("Please enter both Session ID and your message.");
        return;
    }
     
     if (!lockedSessionId) {
        lockedSessionId = sessionId;
        localStorage.setItem("lockedSessionId", sessionId);
    }

    // Add user message to chat
    const userMsgDiv = document.createElement("div");
    userMsgDiv.className = "chat-message user";
    userMsgDiv.textContent = userInput;
    chatBox.appendChild(userMsgDiv);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: userInput
            })
        });

        const data = await response.json();

        // Append bot reply
        const botMsgDiv = document.createElement("div");
        botMsgDiv.className = "chat-message bot";

        const botIcon = document.createElement("div");
        botIcon.className = "bot-icon";
        botIcon.textContent = "🤖";

        const botText = document.createElement("span");
        botText.textContent = data.error ? `Error: ${data.error}` : data.response;

        botMsgDiv.appendChild(botIcon);
        botMsgDiv.appendChild(botText);
        chatBox.appendChild(botMsgDiv);

    } catch (error) {
        const errorDiv = document.createElement("div");
        errorDiv.className = "chat-message bot";
        errorDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
        chatBox.appendChild(errorDiv);
    }

    // Clear the input and scroll to bottom
    document.getElementById("user-input").value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Save updated chat to localStorage
    localStorage.setItem("chatHistory", chatBox.innerHTML);
}

// Load chat from localStorage on page load
window.addEventListener("DOMContentLoaded", () => {
    const savedChat = localStorage.getItem("chatHistory");
    if (savedChat) {
        document.getElementById("chat-box").innerHTML = savedChat;
    }
});

// Clear chat button functionality
function clearChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";
    localStorage.removeItem("chatHistory");
}
